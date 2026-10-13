import {readFileSync,writeFileSync,mkdirSync,existsSync} from 'node:fs';
import assert from 'node:assert/strict';
import type {GenLayerClient,TransactionHash} from 'genlayer-js/types';
import {TransactionHashVariant} from 'genlayer-js/types';
import {studionet} from 'genlayer-js/chains';
import {finalized} from '../lib/domain';
import {rpc} from '../lib/network';
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- JSON-only historical protocol journal, never account or key data.
type Journal=Record<string,any>;
const encode=(v:unknown)=>JSON.stringify(v,(_,x)=>typeof x==='bigint'?String(x):x,2)+'\n';
export async function cleanupLegacy(client:GenLayerClient<typeof studionet>){
  const generation=process.env.FOOTNOTE_STEP==='cleanup-v1'?'v1':'v2';
  const root='docs/legacy/'+generation;
  const deployment:Journal=JSON.parse(readFileSync(root+'/deployment.json','utf8'));
  const addresses=deployment.contracts;
  const wallet=(typeof client.account==='string'?client.account:client.account?.address)?.toLowerCase();
  assert.equal(wallet,'0xdb433ff614bdd1ece21aa97221c3e0a7ecf79c92');
  assert.equal(client.chain?.id,61999);
  const dir=root+'/cleanup';mkdirSync(dir,{recursive:true});
  const file=dir+'/journal.json';
  const p:Journal=existsSync(file)?JSON.parse(readFileSync(file,'utf8')):{generation,contracts:addresses,transactions:{},states:{},balances:{}};
  const save=()=>writeFileSync(file,encode(p));
  assert.ok(!p.failure,'STOP: prior cleanup failure '+p.failure);
  if(p.complete){console.log(generation+' cleanup already complete; preserving the historical balance snapshots.');return;}
  const state=async(method:string,args:Parameters<typeof client.readContract>[0]['args'])=>JSON.parse(String(await client.readContract({address:addresses.bonds,functionName:method,args,transactionHashVariant:TransactionHashVariant.LATEST_FINAL})));
  const balances=async()=>({wallet:String(await client.getBalance({address:wallet!})),bonds:String(await client.getBalance({address:addresses.bonds}))});
  if(!p.balances.start){p.balances.start=await balances();save();}
  async function final(hash:TransactionHash,name:string):Promise<Journal>{
    let raw:Journal|null=null;
    for(let i=0;i<48;i++){
      try{raw=await rpc('eth_getTransactionByHash',[hash]);if(raw?.status==='FINALIZED')break;}catch{ /* Same saved hash on transient polling errors. */ }
      await new Promise(resolve=>setTimeout(resolve,10000));
    }
    assert.ok(raw?.status==='FINALIZED','Polling timeout; resume '+hash+' without resubmission');
    writeFileSync(dir+'/'+name+'.json',encode(raw));
    if(raw.type===0&&raw.consensus_data===null?raw.value_credited!==true:!finalized(raw)){
      p.failure=name+' '+hash;save();throw Error('LIVE CLEANUP FAILURE '+encode(raw.consensus_data??raw));
    }
    console.log(name+' FINALIZED successful '+hash);
    for(const [i,child] of (raw.triggered_transactions??[]).entries()){
      const label=name+'-child-'+i;p.transactions[label]=child;save();await final(child,label);
    }
    return raw;
  }
  async function write(name:string,method:string,args:Parameters<typeof client.writeContract>[0]['args']){
    let hash=p.transactions[name] as TransactionHash|undefined;
    if(!hash){hash=await client.writeContract({address:addresses.bonds,functionName:method,args,value:0n}) as TransactionHash;p.transactions[name]=hash;save();console.log('Persisted '+name+' '+hash);}
    await final(hash,name);return hash;
  }
  const ids=generation==='v2'?['climate-quota-2','climate-quota-3','temperature-update-2025','independent-climate-appeal']:['climate-record','open-question','climate-quota-2','climate-quota-3'];
  for(const id of ids){
    const claimId='bond:'+id;
    if(p.states[claimId]?.status==='paid')continue;
    const bond=await state('get_bond',[id]);
    const releaseAt=bond.release_at??bond.deadline;assert.ok(Number.isInteger(releaseAt));
    if(Date.now()/1000<releaseAt){p.waiting={id,releaseAt,utc:new Date(releaseAt*1000).toISOString()};save();console.log('WAIT: '+encode(p.waiting));return;}
    if(!p.transactions[id+'-release'])assert.equal(await client.readContract({address:addresses.appeals,functionName:'has_open_appeal',args:[id],transactionHashVariant:TransactionHashVariant.LATEST_FINAL}),false,'Open legacy appeal; no release write sent.');
    if(!p.balances[id+'-before']){p.balances[id+'-before']=await balances();save();}
    await write(id+'-release','release',[id]);
    const hash=await write(id+'-withdraw','withdraw',[claimId,1]);
    await write(id+'-verify','verify_claim',[claimId,hash]);
    const claim=await state('get_claim',[claimId]);assert.equal(claim.status,'paid');assert.equal(claim.recipient,wallet);
    const after=await balances(),before=p.balances[id+'-before'];
    assert.equal(BigInt(after.wallet)-BigInt(before.wallet),BigInt(claim.amount));
    assert.equal(BigInt(before.bonds)-BigInt(after.bonds),BigInt(claim.amount));
    p.states[claimId]=claim;p.states[id]=await state('get_bond',[id]);p.balances[id+'-after']=after;save();
  }
  p.balances.end=await balances();p.complete=true;delete p.waiting;save();
  console.log(generation+' cleanup complete, exact balances '+encode(p.balances));
}
