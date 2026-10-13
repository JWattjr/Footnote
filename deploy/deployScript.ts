import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import type {GenLayerClient,TransactionHash} from 'genlayer-js/types';
import {TransactionStatus,TransactionHashVariant} from 'genlayer-js/types';
import {studionet} from 'genlayer-js/chains';
import {finalized,type Addresses} from '../lib/domain';
import {rpc} from '../lib/network';
import {additionalProof} from '../scripts/additional-proof';
import {cleanupLegacy} from '../scripts/cleanup-legacy';
import {spawnSync} from 'node:child_process';
type Proof={network:string;chainId:number;contracts:Addresses;transactions:Record<string,TransactionHash>;states:Record<string,unknown>;proofs:unknown[];preflights?:Record<string,string>;rejections?:Record<string,string>;unproven:string[]};
const file='public/deployment.json';
const encode=(v:unknown)=>JSON.stringify(v,(_,x)=>typeof x==='bigint'?String(x):x,2)+'\n';
export async function deploy(client:GenLayerClient<typeof studionet>){
  if(client.chain?.id!==61999)throw Error('StudioNet 61999 required');
  if(process.env.FOOTNOTE_STEP?.startsWith('cleanup-'))return cleanupLegacy(client);
  if(process.env.FOOTNOTE_STEP?.startsWith('extra-'))return additionalProof(client);
  const p:Proof=JSON.parse(readFileSync(file,'utf8'));mkdirSync('docs/proofs',{recursive:true});
  const save=()=>writeFileSync(file,encode(p));
  const read=async(address:`0x${string}`,method:string,args:Parameters<typeof client.readContract>[0]['args']=[])=>client.readContract({address,functionName:method,args,transactionHashVariant:TransactionHashVariant.LATEST_FINAL});
  async function final(hash:TransactionHash,name:string):Promise<Record<string,unknown>>{
    await client.waitForTransactionReceipt({hash,status:TransactionStatus.FINALIZED,retries:60,interval:5000});
    const raw=await rpc('eth_getTransactionByHash',[hash]);if(!raw)throw Error('Receipt missing');
    writeFileSync('docs/proofs/'+name+'.json',encode(raw));
    const native=raw.type===0&&raw.consensus_data===null;
    if(native?raw.status!=='FINALIZED'||raw.value_credited!==true:!finalized(raw))throw Error('LIVE STEP FAILED '+name+' leader output: '+encode(raw.consensus_data));
    console.log(name+' FINALIZED successful '+hash);return raw;
  }
  async function descendants(hash:TransactionHash,name:string){
    const children=await client.getTriggeredTransactionIds({hash});
    for(const [i,child] of children.entries()){const label=name+'-child-'+i;p.transactions[label]=child as TransactionHash;save();await final(child as TransactionHash,label);await descendants(child as TransactionHash,label);}
  }
  async function deployOne(key:keyof Addresses,args:Parameters<typeof client.deployContract>[0]['args']){
    if(p.contracts[key])return p.contracts[key]!;
    const name='deploy-'+key;let hash=p.transactions[name];
    if(!hash){hash=await client.deployContract({code:readFileSync('contracts/'+key+'.py','utf8'),args}) as TransactionHash;p.transactions[name]=hash;save();console.log('Submitted '+name+' '+hash);}
    const receipt=await final(hash,name);p.contracts[key]=String(receipt.to_address??receipt.recipient) as `0x${string}`;save();return p.contracts[key]!;
  }
  async function write(name:string,address:`0x${string}`,method:string,args:Parameters<typeof client.writeContract>[0]['args'],value=0n){
    let hash=p.transactions[name];
    if(!hash){
      if(method==='create_note'){
        const checked=spawnSync('python',['scripts/preflight-extra.py'],{encoding:'utf8'});
        if(checked.status!==0)throw Error('Off-chain preflight failed; no write sent. '+checked.stdout+checked.stderr);
        writeFileSync('docs/proofs/preflight-'+name+'.json',readFileSync('docs/proofs/extra-inputs.json'));
        p.preflights??={};p.preflights[name]='docs/proofs/preflight-'+name+'.json';save();
      }
      if(value>0n){const account=typeof client.account==='string'?client.account:client.account?.address;const balance=await client.getBalance({address:account!});if(balance<value)throw Error('Insufficient simulated GEN for '+name+'; no write sent. Balance wei '+balance);}
      hash=await client.writeContract({address,functionName:method,args,value});p.transactions[name]=hash;save();console.log('Submitted '+name+' '+hash);
    }
    await final(hash,name);await descendants(hash,name);
    if(!p.proofs.some(point=>(point as {step?:string}).step===name)){
      const values=args??[];const id=String(values[0]);
      let state:Record<string,unknown>|undefined;let expected='';
      if(method==='stake'){state=JSON.parse(String(await read(address,'get_bond',[id])));expected='locked';}
      if(method==='create_note'){state=JSON.parse(String(await read(address,'get_note',[id])));expected='active';}
      if(method==='release'){state=JSON.parse(String(await read(address,'get_bond',[id])));expected='survived';}
      if(method==='withdraw'||method==='verify_claim'){state=JSON.parse(String(await read(address,'get_claim',[id])));expected=method==='withdraw'?'pending':'paid';}
      if(method==='cancel_stale'){state=JSON.parse(String(await read(address,'get_appeal',[id])));expected='CANCELLED';}
      if(state){if(state.status!==expected)throw Error('LIVE STATE CHECK FAILED '+name+' '+encode(state));p.proofs.push({step:name,hash,readAt:new Date().toISOString(),state});save();console.log(name+' finalized state matches '+expected);}
    }
    return hash;
  }
  async function reject(name:string,args:Parameters<typeof client.writeContract>[0]['args'],expected:string,address=p.contracts.notes!,method='create_note'){
    let hash=p.transactions[name];
    if(!hash){hash=await client.writeContract({address,functionName:method,args,value:0n});p.transactions[name]=hash;save();console.log('Submitted expected rejection '+name+' '+hash);}
    await client.waitForTransactionReceipt({hash,status:TransactionStatus.FINALIZED,retries:60,interval:5000});
    const raw=await rpc('eth_getTransactionByHash',[hash]);
    writeFileSync('docs/proofs/'+name+'.json',encode(raw));
    if(!raw||raw.status!=='FINALIZED'||finalized(raw)||!(encode(raw.consensus_data)+Buffer.from(String(((raw.consensus_data as {leader_receipt?:{result?:string}[]})?.leader_receipt?.[0]?.result)??''),'base64').toString()).includes(expected))throw Error('Unexpected rejection receipt '+encode(raw));
    p.rejections??={};p.rejections[name]=expected;save();console.log(name+' FINALIZED expected rejection '+hash+' leader: '+expected);
  }
  const step=process.env.FOOTNOTE_STEP??'deploy';
  if(step==='balance'){const wallet=typeof client.account==='string'?client.account:client.account?.address;console.log('Configured wallet balance wei: '+String(await client.getBalance({address:wallet!})));return;}
  if(step==='deploy'){
    const notes=await deployOne('notes',[JSON.stringify(['en.wikipedia.org','www.bbc.com','www.reuters.com','apnews.com','www.theguardian.com','www.nasa.gov','science.nasa.gov','svs.gsfc.nasa.gov','www.noaa.gov','www.ncei.noaa.gov','climate.copernicus.eu','www.gov.uk','www.justice.gov','europepmc.org','www.ebi.ac.uk']),900]);
    const bonds=await deployOne('bonds',[notes,900,900]);
    const recheck=await deployOne('recheck',[notes]);
    const appeals=await deployOne('appeals',[notes,bonds,900,600]);
    await write('wire-bonds',bonds,'wire',[appeals]);await write('wire-notes',notes,'wire',[recheck,appeals,bonds]);
    p.states.config=JSON.parse(String(await read(notes,'get_config')));
    p.states.bondsConfig=JSON.parse(String(await read(bonds,'get_config')));
    p.states.appealsConfig=JSON.parse(String(await read(appeals,'get_config')));save();return;
  }
  if(!p.contracts.notes||!p.contracts.bonds||!p.contracts.appeals||!p.contracts.recheck)throw Error('Deploy all contracts first');
  const live=JSON.parse(readFileSync('docs/proofs/live-inputs.json','utf8'));
  const selected=process.env.FOOTNOTE_CASE??'supported';const input=live[selected];
  if(!input)throw Error('Unknown live case');
  const wallet=typeof client.account==='string'?client.account:client.account?.address;
  if(step==='core-quota'){
    for(const selectedName of ['quota2','quota3']){
      const sample=live[selectedName];if(!sample.preflightPassed)throw Error('Fresh quota preflight required');
      await write(selectedName+'-stake',p.contracts.bonds,'stake',[sample.id],2n*10n**18n);
      await write(selectedName+'-note',p.contracts.notes,'create_note',[sample.id,sample.uri,JSON.stringify(sample.sources)]);
      const state=JSON.parse(String(await read(p.contracts.notes,'get_note',[sample.id])));p.states[sample.id]=state;save();
      if(state.status!=='active'||!sample.expected.includes(state.history.at(-1).decision.evidence_label))throw Error('Unexpected quota-note judgment '+encode(state));
    }
    const sample=live.supported;
    await reject('reject-quota',['climate-quota-4',sample.uri,JSON.stringify(sample.sources)],'three notes per post per address quota');
    p.states.quota={writer:wallet,uri:sample.uri,value:JSON.parse(String(await read(p.contracts.notes,'get_quota',[wallet!,sample.uri])))};save();return;
  }
  if(step==='reject-open-recheck')await reject('reject-open-recheck',[input.id,'[]'],'[EXPECTED] note has an open appeal; recheck after it is decided',p.contracts.recheck,'recheck');
  if(step==='reject-host'||step==='prove-appeal')await reject('reject-host',['host-rejection',input.uri,JSON.stringify(['https://example.com/footnote-proof'])],'source host is not allowed');
  if(step==='reject-quota'){
    await reject('reject-quota',['climate-quota-4',input.uri,JSON.stringify(input.sources)],'three notes per post per address quota');
    p.states.quota={writer:wallet,uri:input.uri,value:JSON.parse(String(await read(p.contracts.notes,'get_quota',[wallet!,input.uri])))};save();
  }
  if(step==='recheck'){
    await write(selected+'-recheck',p.contracts.recheck,'recheck',[input.id,'[]']);
    p.states[input.id]=JSON.parse(String(await read(p.contracts.notes,'get_note',[input.id])));save();
    p.states.recheck=JSON.parse(String(await read(p.contracts.recheck,'get_operation',['recheck-1'])));save();
  }
  if(step==='stake'||step==='quota-note'||step==='start-appeal')await write(selected+'-stake',p.contracts.bonds,'stake',[input.id],2n*10n**18n);
  if(step==='note'||step==='quota-note'||step==='start-appeal'){
    if(!input.preflightPassed)throw Error('Three identical canonical fetches and exact quote check required');
    await write(selected+'-note',p.contracts.notes,'create_note',[input.id,input.uri,JSON.stringify(input.sources)]);
    const state=JSON.parse(String(await read(p.contracts.notes,'get_note',[input.id])));
    p.states[input.id]=state;save();
    console.log('Note '+input.id+' '+state.history.at(-1).decision.evidence_label+'; real appeal deadline UTC '+new Date(state.deadline*1000).toISOString());
    if(state.status!=='active'||!input.expected.includes(state.history.at(-1).decision.evidence_label))throw Error('Unexpected live judgment '+encode(state));
  }
  if(step==='open-appeal'||step==='appeal'||step==='start-appeal'){
    await write(selected+'-fund-appeal',p.contracts.bonds,'fund_appeal',[input.id,1],2n*10n**18n);
    await write(selected+'-contest',p.contracts.appeals,'contest',[input.id,1,JSON.stringify(input.counterSources??input.sources)]);
    p.states[input.id+':appeal']=JSON.parse(String(await read(p.contracts.appeals,'get_appeal',[input.id+':1'])));save();
  }
  if(step==='decide-appeal'||step==='appeal'||step==='prove-appeal'){
    await write(selected+'-judge',p.contracts.appeals,'judge',[input.id+':1']);
    await write(selected+'-settle',p.contracts.bonds,'settle_appeal',[input.id+':1']);
    p.states[input.id+':appeal']=JSON.parse(String(await read(p.contracts.appeals,'get_appeal',[input.id+':1'])));save();
  }
  if(step==='cancel-stale'){
    const appeal=JSON.parse(String(await read(p.contracts.appeals,'get_appeal',[input.id+':1'])));
    if(!p.transactions[selected+'-cancel-stale']&&Date.now()/1000<appeal.deadline+600)throw Error('Cancellation is not mature; no write sent. UTC '+new Date((appeal.deadline+600)*1000).toISOString());
    await write(selected+'-cancel-stale',p.contracts.appeals,'cancel_stale',[input.id+':1']);
    p.states[input.id+':appeal']=JSON.parse(String(await read(p.contracts.appeals,'get_appeal',[input.id+':1'])));save();
  }
  if(step==='withdraw-deposit'||step==='withdraw-both'){
    const claim='deposit:'+input.id+':1';
    if(!p.states[claim+':balances']){p.states[claim+':balances']={before:String(await client.getBalance({address:wallet!}))};save();}
    const hash=await write(selected+'-withdraw-deposit',p.contracts.bonds,'withdraw',[claim,1]);
    await write(selected+'-verify-deposit',p.contracts.bonds,'verify_claim',[claim,hash]);
    p.states[claim]=JSON.parse(String(await read(p.contracts.bonds,'get_claim',[claim])));
    p.states[claim+':balances']={...(p.states[claim+':balances'] as object),after:String(await client.getBalance({address:wallet!}))};save();
  }
  if(step==='withdraw-bond'||step==='withdraw-both'){
    if(!p.transactions[selected+'-release']){const bond=JSON.parse(String(await read(p.contracts.bonds,'get_bond',[input.id])));if(Date.now()/1000<bond.release_at)throw Error('Bond is not mature; no write sent. Deadline UTC: '+new Date(bond.release_at*1000).toISOString());}
    await write(selected+'-release',p.contracts.bonds,'release',[input.id]);
    const claim='bond:'+input.id;
    if(!p.states[claim+':balances']){p.states[claim+':balances']={before:String(await client.getBalance({address:wallet!}))};save();}
    const hash=await write(selected+'-withdraw-bond',p.contracts.bonds,'withdraw',[claim,1]);
    await write(selected+'-verify-bond',p.contracts.bonds,'verify_claim',[claim,hash]);
    p.states[claim]=JSON.parse(String(await read(p.contracts.bonds,'get_claim',[claim])));
    p.states[claim+':balances']={...(p.states[claim+':balances'] as object),after:String(await client.getBalance({address:wallet!}))};
    p.states[input.id]=JSON.parse(String(await read(p.contracts.notes,'get_note',[input.id])));save();
  }
}
export default deploy;
