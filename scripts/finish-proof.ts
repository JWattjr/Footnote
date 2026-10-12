import {readFileSync,writeFileSync} from 'node:fs';
import {read,readClient} from '../lib/network';
import type {Addresses,Note} from '../lib/domain';
const p=JSON.parse(readFileSync('public/deployment.json','utf8'));
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
const outstanding=[];
for(const id of ids){
  const bond=p.states['escrowBond:'+id];
  if(bond.status==='locked')outstanding.push({id,amount:bond.amount,releaseAt:bond.release_at,hasOpenAppeal:await read(addresses.appeals,'has_open_appeal',[id]),mature:Date.now()/1000>=bond.release_at});
}
p.accounting.outstandingBonds=outstanding;
p.unproven=['Forced version-drift cancellation, adversarial callback failures/replays and distinct recipient accounting are direct-test-only.','The changed-source evidence-label replay is test-only; no real publisher correction is claimed.'];
for(const required of ['supported-note','unsupported-note','supported-judge','supported-settle','reject-host','reject-quota','reject-open-recheck'])if(!p.transactions[required])p.unproven.push('Core proof step '+required+' is incomplete live.');
if(!p.transactions['unsupported-cancel-stale'])p.unproven.push('Timeout cancel_stale is not demonstrated live.');
if(!p.states['bond:climate-record']||p.states['bond:climate-record'].status!=='paid')p.unproven.push('Writer-bond withdrawal with verified native credit is not yet complete live.');
if(outstanding.length)p.unproven.push('Quota-note writer bonds remain unwithdrawn: '+outstanding.map(b=>b.id+' ('+b.amount+' wei; mature='+b.mature+', open appeal='+b.hasOpenAppeal+')').join('; ')+'. The core supported and cancelled-note bonds are withdrawn separately.');
p.completedAt=new Date().toISOString();
writeFileSync('public/deployment.json',JSON.stringify(p,null,2)+'\n');
console.log('Final state refreshed; Bonds balance '+balance+' wei; totals '+JSON.stringify(totals));
