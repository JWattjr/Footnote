import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {rpc,read,readClient} from '../lib/network';
import {finalized} from '../lib/domain';
async function readable<T>(label:string,call:()=>Promise<T>):Promise<T>{
  for(let attempt=0;;attempt++){
    try{return await call();}
    catch(error){
      if(attempt>=2)throw new Error('Legacy read unavailable: '+label,{cause:error});
      console.log('Retrying the same read-only legacy request: '+label);
      await new Promise(resolve=>setTimeout(resolve,(attempt+1)*1000));
    }
  }
}
export async function verifyLegacyCleanup(path:string){
  const p=JSON.parse(readFileSync(path,'utf8'));
  assert.equal(p.complete,true,'Legacy cleanup is still pending: '+path);
  const all=new Set(Object.values(p.transactions));
  for(const [name,hash] of Object.entries(p.transactions)){
    const receipt=await readable(name,()=>rpc('eth_getTransactionByHash',[hash]));
    assert.ok(receipt,name+' missing receipt');
    if(receipt.type===0&&receipt.consensus_data===null){assert.equal(receipt.status,'FINALIZED');assert.equal(receipt.value_credited,true);}
    else assert.ok(finalized(receipt),name+' failed');
    for(const child of (receipt.triggered_transactions??[]) as string[])assert.ok(all.has(child),name+' undocumented child');
  }
  for(const [id,expected] of Object.entries(p.states)){
    const actual=await readable(id,async()=>JSON.parse(String(await read(p.contracts.bonds,id.startsWith('bond:')?'get_claim':'get_bond',[id]))));
    assert.deepEqual(actual,expected,id+' historical cleanup state differs');
    if(id.startsWith('bond:')){
      const claim=actual as {status:string;amount:string};assert.equal(claim.status,'paid');
      const target=id.slice(5),before=p.balances[target+'-before'],after=p.balances[target+'-after'];
      assert.equal(BigInt(after.wallet)-BigInt(before.wallet),BigInt(claim.amount));
      assert.equal(BigInt(before.bonds)-BigInt(after.bonds),BigInt(claim.amount));
    }
  }
  assert.equal(String(await readable('Bonds balance',()=>readClient().getBalance({address:p.contracts.bonds}))),p.balances.end.bonds);
  // Main wallet subsequently participates in v3: compare the historical recorded deltas, not its obsolete snapshot.
  console.log(path+' verified all receipts, exact claim credits and final legacy escrow balance.');
}
