import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {rpc} from '../lib/network';

// Later wallet activity must never rewrite the original outcome balance table.
export async function verifyPostProofAccounting(){
  const deployment=JSON.parse(readFileSync('public/deployment.json','utf8'));
  const bridge=deployment.postProofAccounting;
  const historical=deployment.additionalProofs.balances.finish;
  if(!bridge)return historical;
  assert.deepEqual(bridge.historicalFinish,historical);
  const activity=JSON.parse(readFileSync(bridge.externalActivity.path,'utf8'));
  const wallet=deployment.additionalProofs.walletA;
  assert.equal(activity.wallet,wallet);
  const hashes=new Set<string>();let outflow=0n;
  for(const row of activity.rows){
    assert.ok(!hashes.has(row.hash),'Duplicate external accounting receipt');hashes.add(row.hash);
    const receipt=await rpc('eth_getTransactionByHash',[row.hash]);
    assert.ok(receipt);assert.equal(receipt.status,'FINALIZED');assert.equal(receipt.value_credited,true);
    assert.equal(String(receipt.from_address).toLowerCase(),wallet);
    assert.equal(String(receipt.to_address).toLowerCase(),row.to.toLowerCase());
    assert.equal(String(receipt.value),String(row.value));assert.ok(BigInt(String(receipt.value))>0n);
    assert.equal(receipt.created_at,row.created_at);
    assert.ok(Date.parse(row.created_at)>Date.parse(deployment.additionalProofs.completedAt));
    assert.ok(Date.parse(row.created_at)<Date.parse(bridge.externalActivity.before));
    // These are credited outflows only; no claim about the unrelated contract's judgment.
    outflow+=BigInt(String(receipt.value));
  }
  assert.equal(String(outflow),activity.netOutflowWei);
  assert.equal(String(outflow),bridge.externalActivity.netOutflowWei);
  let credits=0n;let running=BigInt(historical.walletA)-outflow;
  const paths=new Set<string>(),creditHashes=new Set<string>();
  for(const path of bridge.recoveries as string[]){
    assert.ok(!paths.has(path),'Duplicate recovery journal');paths.add(path);
    assert.ok(deployment.legacyCleanup.includes(path),'Recovery is not independently network-verified');
    const recovery=JSON.parse(readFileSync(path,'utf8'));
    assert.equal(recovery.complete,true);assert.equal(BigInt(recovery.balances.start.wallet),running);
    let refunded=0n;
    for(const [id,claim] of Object.entries(recovery.states) as [string,{status:string;recipient:string;amount:string;transfer_hash:string}][]){
      if(!id.startsWith('bond:'))continue;
      assert.equal(claim.status,'paid');assert.equal(claim.recipient,wallet);
      assert.ok(!creditHashes.has(claim.transfer_hash),'Recovery native credit counted twice');creditHashes.add(claim.transfer_hash);
      assert.ok(Object.values(recovery.transactions).includes(claim.transfer_hash));
      refunded+=BigInt(claim.amount);
    }
    assert.equal(BigInt(recovery.balances.end.wallet)-running,refunded);
    assert.equal(BigInt(recovery.balances.start.bonds)-BigInt(recovery.balances.end.bonds),refunded);
    running+=refunded;credits+=refunded;
  }
  assert.equal(String(credits),bridge.verifiedRecoveryCreditsWei);
  assert.equal(String(running),bridge.current.walletA);
  assert.equal(bridge.current.walletB,historical.walletB);
  assert.equal(bridge.current.bonds,historical.bonds);
  console.log('Historical v3 balances retained; later credited outflows and verified legacy refunds reconcile current wallet balances.');
  return bridge.current as {walletA:string;walletB:string;bonds:string};
}
