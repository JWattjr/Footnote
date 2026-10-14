import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {rpc,readClient} from '../lib/network';
import {verificationRead as read} from './verification-read';
import {verifyPostProofAccounting} from './verify-post-proof-accounting';

export async function verifyAdditionalProofs(currentBalances?:{walletA:string;walletB:string;bonds:string}){
  const p=JSON.parse(readFileSync('public/deployment.json','utf8'));
  const e=p.additionalProofs;
  assert.ok(e.completedAt,'Additional live proof is incomplete; do not claim it passed.');
  assert.notEqual(e.walletA,e.walletB);
  assert.equal(p.quotaRejectionSnapshot.value.per_post,3,'Historical saturated quota snapshot missing');
  assert.equal(p.quotaRejectionSnapshot.writer.toLowerCase(),e.walletA);
  type Check={quote:string;fetches:{status:number;digest:string;quotePresent:boolean}[];supportedClaimChecks?:Check[]};
  function verifyCheck(check:Check){
    assert.equal(check.fetches.length,3);assert.ok(check.quote);
    assert.ok(check.fetches.every(f=>f.status===200&&f.quotePresent));
    assert.equal(new Set(check.fetches.map(f=>f.digest)).size,1);
    for(const item of check.supportedClaimChecks??[])verifyCheck(item);
  }
  const inputs=JSON.parse(readFileSync(e.inputs,'utf8'));
  for(const check of Object.values(inputs.checks) as Check[])verifyCheck(check);
  for(const step of ['extra-independent-note','extra-change-note','extra-change-recheck','quota2-note','quota3-note']){
    assert.ok(p.preflights[step],step+' has no pre-write preflight');
    const checked=JSON.parse(readFileSync(p.preflights[step],'utf8'));
    for(const check of Object.values(checked.checks) as Check[])verifyCheck(check);
  }
  const note=JSON.parse(String(await read(p.contracts.notes,'get_note',[e.labelChange.noteId])));
  assert.equal(note.version,2);assert.equal(note.history.length,2);
  assert.equal(note.history[0].decision.evidence_label,'UNSUPPORTED');
  assert.equal(note.history[1].decision.evidence_label,'SUPPORTED');
  assert.equal(note.history[1].reason,'RECHECK');
  assert.ok(note.history[1].decision.citations.some((c:{url:string})=>inputs.cases.labelChange.addedSources.includes(c.url)));
  assert.deepEqual(note.history[0],e.labelChange.before.history[0]);
  const op=JSON.parse(String(await read(p.contracts.recheck,'get_operation',[e.labelChange.operation])));
  assert.equal(op.status,'finalized');assert.equal(op.outcome,'UPDATED');
  assert.equal(op.note_id,note.id);assert.equal(op.version,1);
  assert.equal(await read(p.contracts.appeals,'has_open_appeal',[note.id]),false);
  const appealId=e.twoWallet.noteId+':1';
  const appeal=JSON.parse(String(await read(p.contracts.appeals,'get_appeal',[appealId])));
  assert.equal(appeal.writer,e.walletA);assert.equal(appeal.appellant,e.walletB);assert.equal(appeal.status,'settled');
  assert.ok(['UPHELD','OVERTURNED'].includes(appeal.outcome));
  assert.equal(await read(p.contracts.appeals,'has_open_appeal',[e.twoWallet.noteId]),false);
  const fund=await rpc('eth_getTransactionByHash',[p.transactions['extra-fund-wallet-b']]);
  assert.equal(fund?.status,'FINALIZED');assert.equal(fund?.value_credited,true);
  assert.equal(String(fund?.from_address).toLowerCase(),e.walletA);assert.equal(String(fund?.to_address).toLowerCase(),e.walletB);
  assert.equal(String(fund?.value),'2000000000000000000');
  for(const [step,expected] of Object.entries(e.steps) as [string,{hash:string;signer:string}][]){
    const receipt=await rpc('eth_getTransactionByHash',[expected.hash]);
    assert.equal(receipt?.status,'FINALIZED');assert.equal(String(receipt?.from_address).toLowerCase(),expected.signer,step);
    assert.equal(expected.signer,['extra-independent-fund-appeal','extra-independent-contest'].includes(step)?e.walletB:step.includes('-deposit-')||step.includes('independent-bond-withdraw')||step.includes('independent-bond-verify')?appeal.outcome==='UPHELD'?e.walletA:e.walletB:e.walletA,step);
  }
  const client=readClient();
  const finish=e.balances.finish;
  const current=currentBalances??await verifyPostProofAccounting();
  assert.equal(String(await client.getBalance({address:e.walletA})),current.walletA);
  assert.equal(String(await client.getBalance({address:e.walletB})),current.walletB);
  assert.equal(String(await client.getBalance({address:p.contracts.bonds})),current.bonds);
  const gen=10n**18n;
  const before=e.balances['funding-before'],after=e.balances['funding-after'];
  const fee=BigInt(e.fundingFeeWei??'0');
  assert.equal(BigInt(before.walletA)-BigInt(after.walletA),2n*gen+fee);
  assert.equal(BigInt(after.walletB)-BigInt(before.walletB),2n*gen);
  const start=e.balances.start;
  const deltaA=appeal.outcome==='UPHELD'?0n:-4n*gen;
  const deltaB=-deltaA;
  assert.equal(BigInt(finish.walletA)-BigInt(start.walletA),deltaA-fee);
  assert.equal(BigInt(finish.walletB)-BigInt(start.walletB),deltaB);
  assert.equal(finish.bonds,start.bonds);
  assert.equal(BigInt(start.walletA)+BigInt(start.walletB)+BigInt(start.bonds)-fee,BigInt(finish.walletA)+BigInt(finish.walletB)+BigInt(finish.bonds));
  const totals=JSON.parse(String(await read(p.contracts.bonds,'get_totals')));
  assert.equal(BigInt(totals.received)-BigInt(totals.paid),BigInt(finish.bonds));
  console.log('Additional proofs verified: preserved UNSUPPORTED → SUPPORTED history, distinct signing wallets, funding and exact outcome balances.');
}
