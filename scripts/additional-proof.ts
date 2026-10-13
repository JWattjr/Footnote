import {readFileSync,writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import type {GenLayerClient,TransactionHash} from 'genlayer-js/types';
import {TransactionHashVariant} from 'genlayer-js/types';
import {studionet} from 'genlayer-js/chains';
import {finalized} from '../lib/domain';
import {rpc} from '../lib/network';

const A='0xdb433ff614bdd1ece21aa97221c3e0a7ecf79c92';
const B='0xbc1a363b1427531fcb05d03ddf4d34e729011186';
const GEN=10n**18n;
type Address=`0x${string}`;
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- Persist heterogeneous raw protocol/state records without copying signing-account objects.
type Json=Record<string,any>;
const encode=(value:unknown)=>JSON.stringify(value,(_,x)=>typeof x==='bigint'?String(x):x,2)+'\n';

export async function additionalProof(client:GenLayerClient<typeof studionet>){
  assert.equal(client.chain?.id,61999);
  const p:Json=JSON.parse(readFileSync('public/deployment.json','utf8'));
  const inputs:Json=JSON.parse(readFileSync('docs/proofs/extra-inputs.json','utf8'));
  assert.equal(p.generation,3,'Fresh consensus-fixed deployment required.');
  assert.equal(Object.keys(p.contracts).length,4);
  const addresses=p.contracts as Record<'notes'|'bonds'|'recheck'|'appeals',Address>;
  const account=client.account;
  const wallet=(typeof account==='string'?account:account?.address)?.toLowerCase();
  assert.ok(wallet===A||wallet===B,'Only the two recorded public proof wallets may sign.');
  p.additionalProofs??={startedAt:new Date().toISOString(),walletA:A,walletB:B,inputs:'docs/proofs/extra-inputs.json',steps:{},balances:{},labelChange:{noteId:inputs.cases.labelChange.id},twoWallet:{noteId:inputs.cases.twoWallet.id}};
  const extra=p.additionalProofs;
  const save=()=>writeFileSync('public/deployment.json',encode(p));
  const read=async(address:Address,method:string,args:Parameters<typeof client.readContract>[0]['args']=[])=>client.readContract({address,functionName:method,args,transactionHashVariant:TransactionHashVariant.LATEST_FINAL});
  const state=async(address:Address,method:string,args:Parameters<typeof client.readContract>[0]['args']=[])=>JSON.parse(String(await read(address,method,args)));
  const balances=async()=>({walletA:String(await client.getBalance({address:A})),walletB:String(await client.getBalance({address:B})),bonds:String(await client.getBalance({address:addresses.bonds}))});
  const snapshot=async(name:string)=>{if(!extra.balances[name]){extra.balances[name]={at:new Date().toISOString(),...await balances()};save();}return extra.balances[name];};
  const assertRole=(expected:string)=>assert.equal(wallet,expected,'Wrong configured CLI account; no write sent.');
  if(extra.failure)throw Error('STOP: previous live failure is recorded; no more writes. '+extra.failure);
  await snapshot('start');

  async function final(hash:TransactionHash,name:string){
    let raw:Record<string,unknown>|null=null;
    for(let attempt=0;attempt<48;attempt++){
      try{raw=await rpc('eth_getTransactionByHash',[hash]);if(raw?.status==='FINALIZED')break;}
      catch(error){if(attempt===0)console.log('Receipt polling unavailable; keeping the same hash '+hash+': '+(error as Error).message);}
      await new Promise(resolve=>setTimeout(resolve,10000));
    }
    if(raw?.status!=='FINALIZED')throw Error('Receipt polling timed out; resume the same hash '+hash+'; no resubmission.');
    writeFileSync('docs/proofs/'+name+'.json',encode(raw));
    const native=raw?.type===0&&raw.consensus_data===null;
    if(!raw||(native?raw.status!=='FINALIZED'||raw.value_credited!==true:!finalized(raw))){
      extra.failure=name+' '+hash;save();
      throw Error('LIVE FAILURE '+name+' exact leader output: '+encode(raw?.consensus_data??raw));
    }
    console.log(name+' FINALIZED successful '+hash);
    return raw;
  }
  async function descendants(hash:TransactionHash,name:string){
    const receipt=JSON.parse(readFileSync('docs/proofs/'+name+'.json','utf8'));
    for(const [i,child] of (receipt.triggered_transactions as TransactionHash[]).entries()){
      const label=name+'-child-'+i;p.transactions[label]=child;save();
      await final(child as TransactionHash,label);await descendants(child as TransactionHash,label);
    }
  }
  async function write(name:string,address:Address,method:string,args:Parameters<typeof client.writeContract>[0]['args'],value=0n){
    let hash=p.transactions[name] as TransactionHash|undefined;
    if(!hash){
      if(method==='create_note'||method==='recheck'){
        const checked=spawnSync('python',['scripts/preflight-extra.py'],{encoding:'utf8'});
        assert.equal(checked.status,0,'Off-chain preflight failed; no write sent. '+checked.stdout+checked.stderr);
        const path='docs/proofs/preflight-'+name+'.json';writeFileSync(path,readFileSync(extra.inputs));
        p.preflights??={};p.preflights[name]=path;save();console.log('Fresh three-fetch preflight saved '+path);
      }
      if(value>0n)assert.ok(await client.getBalance({address:wallet as Address})>=value,'Insufficient balance; no write sent.');
      hash=await client.writeContract({address,functionName:method,args,value}) as TransactionHash;
      p.transactions[name]=hash;save();console.log('Persisted '+name+' '+hash);
    }
    await final(hash,name);await descendants(hash,name);
    extra.steps[name]={hash,finalizedAt:new Date().toISOString(),signer:wallet};save();return hash;
  }
  async function rememberNote(id:string){const note=await state(addresses.notes,'get_note',[id]);p.states[id]=note;p.states['escrowBond:'+id]=await state(addresses.bonds,'get_bond',[id]);save();return note;}
  async function expectLabel(id:string,label:string,version:number){
    const note=await rememberNote(id);
    if(note.status!=='active'||note.version!==version||note.history.at(-1).decision.evidence_label!==label){
      extra.failure='Unexpected finalized label/version for '+id;save();
      throw Error('STOP: '+extra.failure+'; exact finalized decision: '+encode(note.history.at(-1).decision));
    }
    return note;
  }
  async function paid(claimId:string,prefix:string,recipient:string){
    assertRole(recipient);
    const before=await snapshot(prefix+'-before');
    const hash=await write(prefix+'-withdraw',addresses.bonds,'withdraw',[claimId,1]);
    await write(prefix+'-verify',addresses.bonds,'verify_claim',[claimId,hash]);
    const claim=await state(addresses.bonds,'get_claim',[claimId]);
    assert.equal(claim.status,'paid');assert.equal(claim.recipient,recipient);
    const after=await snapshot(prefix+'-after');
    const role=recipient===A?'walletA':'walletB';
    assert.equal(BigInt(after[role])-BigInt(before[role]),BigInt(claim.amount));
    assert.equal(BigInt(before.bonds)-BigInt(after.bonds),BigInt(claim.amount));
    p.states[claimId]=claim;p.states[claimId+':balances']={before:before[role],after:after[role]};save();
  }
  const step=process.env.FOOTNOTE_STEP;
  const change=inputs.cases.labelChange;
  const challenge=inputs.cases.twoWallet;
  if(step==='extra-inspect'){
    console.log('Wallet roles and balances '+encode({wallet,A,B,balances:await balances()}));
    console.log('Initial quota '+encode(await state(addresses.notes,'get_quota',[A,change.uri])));
    console.log('Appeal quota '+encode(await state(addresses.notes,'get_quota',[A,challenge.uri])));return;
  }
  if(step==='extra-fund-wallet'){
    assertRole(A);
    const name='extra-fund-wallet-b';let hash=p.transactions[name] as TransactionHash|undefined;
    if(!hash){
      assert.ok(account&&typeof account!=='string'&&typeof account.signTransaction==='function');
      const before=await snapshot('funding-before');
      assert.ok(BigInt(before.walletA)>=2n*GEN,'Enough main-wallet backing required for the independent deposit.');
      const nonce=await client.getCurrentNonce({address:A});
      const request=await client.prepareTransactionRequest({account,to:B,value:2n*GEN,type:'legacy',nonce:Number(nonce)});
      const serializedTransaction=await account.signTransaction(request);
      hash=await client.sendRawTransaction({serializedTransaction}) as TransactionHash;
      p.transactions[name]=hash;save();console.log('Persisted '+name+' '+hash);
    }
    await final(hash,name);
    const after=await snapshot('funding-after');const before=extra.balances['funding-before'];
    const fee=BigInt(before.walletA)-BigInt(after.walletA)-2n*GEN;
    assert.ok(fee>=0n);extra.fundingFeeWei=String(fee);
    assert.equal(BigInt(after.walletB)-BigInt(before.walletB),2n*GEN);
    assert.equal(after.bonds,before.bonds);extra.steps[name]={hash,finalizedAt:new Date().toISOString(),signer:A};save();return;
  }
  if(step==='extra-create-unsupported'){
    assertRole(A);await snapshot('label-change-before');
    await write('extra-change-stake',addresses.bonds,'stake',[change.id],2n*GEN);
    await write('extra-change-note',addresses.notes,'create_note',[change.id,change.uri,JSON.stringify(change.initialSources)]);
    const note=await expectLabel(change.id,'UNSUPPORTED',1);extra.labelChange.before=note;save();return;
  }
  if(step==='extra-recheck'){
    assertRole(A);assert.equal(await read(addresses.appeals,'has_open_appeal',[change.id]),false);
    if(!p.transactions['extra-change-recheck'])await expectLabel(change.id,'UNSUPPORTED',1);
    await write('extra-change-recheck',addresses.recheck,'recheck',[change.id,JSON.stringify(change.addedSources)]);
    const note=await expectLabel(change.id,'SUPPORTED',2);
    assert.equal(note.history[0].decision.evidence_label,'UNSUPPORTED');
    assert.ok(note.history[1].decision.citations.some((c:Json)=>change.addedSources.includes(c.url)),'New credible source must be cited.');
    const operation=note.history[1].operation;
    extra.labelChange.after=note;extra.labelChange.operation=operation;
    extra.labelChange.finalizedAt=new Date().toISOString();p.states.recheck=await state(addresses.recheck,'get_operation',[operation]);save();return;
  }
  if(step==='extra-create-appeal-note'){
    assertRole(A);await snapshot('two-wallet-before');
    await write('extra-independent-stake',addresses.bonds,'stake',[challenge.id],2n*GEN);
    await write('extra-independent-note',addresses.notes,'create_note',[challenge.id,challenge.uri,JSON.stringify(challenge.initialSources)]);
    const note=await expectLabel(challenge.id,'SUPPORTED',1);extra.twoWallet.before=note;save();
    console.log('Actual appeal deadline UTC '+new Date(note.deadline*1000).toISOString());return;
  }
  if(step==='extra-open-appeal'){
    assertRole(B);assert.ok(extra.twoWallet.before);
    await write('extra-independent-fund-appeal',addresses.bonds,'fund_appeal',[challenge.id,1],2n*GEN);
    await write('extra-independent-contest',addresses.appeals,'contest',[challenge.id,1,JSON.stringify(challenge.counterSources)]);
    const appeal=await state(addresses.appeals,'get_appeal',[challenge.id+':1']);
    assert.equal(appeal.appellant,B);assert.equal(appeal.writer,A);assert.equal(appeal.status,'open');
    p.states[challenge.id+':appeal']=appeal;extra.twoWallet.open=appeal;save();return;
  }
  if(step==='extra-judge-settle'){
    assertRole(A);
    await write('extra-independent-judge',addresses.appeals,'judge',[challenge.id+':1']);
    const decided=await state(addresses.appeals,'get_appeal',[challenge.id+':1']);
    if(!['UPHELD','OVERTURNED'].includes(decided.outcome)){
      extra.failure='Independent appeal outcome '+decided.outcome;save();throw Error('STOP: '+extra.failure+' exact output '+encode(decided));
    }
    await write('extra-independent-settle',addresses.bonds,'settle_appeal',[challenge.id+':1']);
    const appeal=await state(addresses.appeals,'get_appeal',[challenge.id+':1']);
    assert.equal(appeal.status,'settled');assert.equal(await read(addresses.appeals,'has_open_appeal',[challenge.id]),false);
    p.states[challenge.id+':appeal']=appeal;
    p.states['escrowDeposit:'+challenge.id+':1']=await state(addresses.bonds,'get_deposit',[challenge.id+':1']);
    p.states['fundingRecord:'+appeal.funding_id]=await state(addresses.bonds,'get_funding',[appeal.funding_id]);
    extra.twoWallet.decided=appeal;await rememberNote(challenge.id);await snapshot('two-wallet-settled');save();return;
  }
  if(step==='extra-withdraw-deposit'){
    const recipient=extra.twoWallet.decided.outcome==='UPHELD'?A:B;
    await paid('deposit:'+challenge.id+':1','extra-independent-deposit',recipient);return;
  }
  if(step==='extra-release-change'||step==='extra-release-independent'){
    const isChange=step==='extra-release-change';const id=isChange?change.id:challenge.id;const prefix=isChange?'extra-change-bond':'extra-independent-bond';
    const bond=await state(addresses.bonds,'get_bond',[id]);
    const recipient=bond.status==='overturned'?B:A;assertRole(recipient);
    if(!p.transactions[prefix+'-release']&&bond.status!=='overturned'){
      if(Date.now()/1000<bond.release_at){console.log('WAIT: real bond release time UTC '+new Date(bond.release_at*1000).toISOString());return;}
      assert.equal(await read(addresses.appeals,'has_open_appeal',[id]),false);
    }
    if(bond.status!=='overturned')await write(prefix+'-release',addresses.bonds,'release',[id]);
    await paid('bond:'+id,prefix,recipient);
    await rememberNote(id);save();return;
  }
  throw Error('Unknown additional proof step; no write sent.');
}
