import {readFileSync,writeFileSync} from 'node:fs';
import {read,readClient} from '../lib/network';
import type {Addresses,Note} from '../lib/domain';
const p=JSON.parse(readFileSync('public/deployment.json','utf8'));
if(p.transactions['reject-quota']&&p.states.quota&&!p.quotaRejectionSnapshot)p.quotaRejectionSnapshot=JSON.parse(JSON.stringify(p.states.quota));
const addresses=p.contracts as Required<Addresses>;
const ids=await read(addresses.notes,'list_notes',[0,50]) as string[];
for(const id of ids){
  const note=JSON.parse(String(await read(addresses.notes,'get_note',[id]))) as Note;
  p.states[id]=note;
  p.states['escrowBond:'+id]=JSON.parse(String(await read(addresses.bonds,'get_bond',[id])));
}
for(const key of Object.keys(p.states)){
  if(key.endsWith(':appeal')){
    const id=key.slice(0,-7)+':1';
    const appeal=JSON.parse(String(await read(addresses.appeals,'get_appeal',[id])));
    p.states[key]=appeal;
    p.states['escrowDeposit:'+id]=JSON.parse(String(await read(addresses.bonds,'get_deposit',[id])));
    p.states['fundingRecord:'+appeal.funding_id]=JSON.parse(String(await read(addresses.bonds,'get_funding',[appeal.funding_id])));
  }else if((key.startsWith('bond:')||key.startsWith('deposit:'))&&!key.endsWith(':balances')){
    p.states[key]=JSON.parse(String(await read(addresses.bonds,'get_claim',[key])));
  }else if(key==='quota'){
    p.states.quota.value=JSON.parse(String(await read(addresses.notes,'get_quota',[p.states.quota.writer,p.states.quota.uri])));
  }
}
const wallet=p.states[ids[0]].writer as `0x${string}`;
const client=readClient();
const totals=JSON.parse(String(await read(addresses.bonds,'get_totals')));
const balance=String(await client.getBalance({address:addresses.bonds}));
if(BigInt(balance)!==BigInt(totals.received)-BigInt(totals.paid))throw Error('Bonds balance does not equal received minus verified paid');
p.accounting={wallet,walletBalance:String(await client.getBalance({address:wallet})),bondsBalance:balance,totals};
if(p.additionalProofs){
  const e=p.additionalProofs;
  if(e.failure)throw Error('Additional live failure recorded: '+e.failure);
  const changed=p.states[e.labelChange.noteId];
  if(changed?.version!==2||changed.history[0].decision.evidence_label!=='UNSUPPORTED'||changed.history[1].decision.evidence_label!=='SUPPORTED')throw Error('Live label-change proof is incomplete');
  const appeal=p.states[e.twoWallet.noteId+':appeal'];
  if(appeal?.status!=='settled'||appeal.writer!==e.walletA||appeal.appellant!==e.walletB||!['UPHELD','OVERTURNED'].includes(appeal.outcome))throw Error('Distinct-wallet appeal proof is incomplete');
  for(const claim of ['bond:'+e.labelChange.noteId,'bond:'+e.twoWallet.noteId,'deposit:'+e.twoWallet.noteId+':1'])if(p.states[claim]?.status!=='paid')throw Error('Missing verified additional native withdrawal: '+claim);
  e.balances.finish={at:new Date().toISOString(),walletA:String(await client.getBalance({address:e.walletA})),walletB:String(await client.getBalance({address:e.walletB})),bonds:balance};
  const start=e.balances.start,finish=e.balances.finish,gen=10n**18n;
  const payoutDelta=appeal.outcome==='UPHELD'?0n:-4n*gen;
  const fee=BigInt(e.fundingFeeWei??'0');
  if(BigInt(finish.walletA)-BigInt(start.walletA)!==payoutDelta-fee||BigInt(finish.walletB)-BigInt(start.walletB)!==-payoutDelta||finish.bonds!==start.bonds)throw Error('Additional exact outcome balances differ');
  e.completedAt=new Date().toISOString();
}
const outstanding=[];
for(const id of ids){
  const bond=p.states['escrowBond:'+id];
  if(bond.status==='locked')outstanding.push({id,amount:bond.amount,releaseAt:bond.release_at,hasOpenAppeal:await read(addresses.appeals,'has_open_appeal',[id]),mature:Date.now()/1000>=bond.release_at});
}
p.accounting.outstandingBonds=outstanding;
p.unproven=['Forced version-drift cancellation and adversarial callback failures/replays remain direct-test-only.','Same-URL publisher correction in /replay remains test-only. The live recheck adds an existing credible source; it does not claim a publisher edited or newly published that page.'];
if(!p.additionalProofs?.completedAt)p.unproven.push('A live label change and distinct signing-wallet appeal are not yet complete.');
const core=p.generation===3?['extra-independent-note','extra-change-note','extra-independent-judge','extra-independent-settle','reject-host','reject-quota','reject-open-recheck']:['supported-note','unsupported-note','supported-judge','supported-settle','reject-host','reject-quota','reject-open-recheck'];
for(const required of core)if(!p.transactions[required])p.unproven.push('Core proof step '+required+' is incomplete live.');
if(!p.transactions['unsupported-cancel-stale'])p.unproven.push('Timeout cancel_stale is proven on archived v2; it has not been repeated on this deployment.');
const coreBond='bond:'+(p.generation===3?p.additionalProofs.twoWallet.noteId:'climate-record');
if(p.states[coreBond]?.status!=='paid')p.unproven.push('Writer-bond withdrawal with verified native credit is not yet complete live.');
if(outstanding.length)p.unproven.push('Quota-note writer bonds remain unwithdrawn: '+outstanding.map(b=>b.id+' ('+b.amount+' wei; mature='+b.mature+', open appeal='+b.hasOpenAppeal+')').join('; ')+'. The core supported and cancelled-note bonds are withdrawn separately.');
p.completedAt??=new Date().toISOString();
writeFileSync('public/deployment.json',JSON.stringify(p,null,2)+'\n');
console.log('Final state refreshed; Bonds balance '+balance+' wei; totals '+JSON.stringify(totals));
