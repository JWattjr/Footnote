import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import type {GenLayerClient,TransactionHash} from 'genlayer-js/types';
import {TransactionStatus,TransactionHashVariant} from 'genlayer-js/types';
import {studionet} from 'genlayer-js/chains';
import {finalized,type Addresses} from '../lib/domain';
import {rpc} from '../lib/network';
type Proof={network:string;chainId:number;contracts:Addresses;transactions:Record<string,TransactionHash>;states:Record<string,unknown>;proofs:unknown[];rejections?:Record<string,string>;unproven:string[]};
const file='public/deployment.json';
const encode=(v:unknown)=>JSON.stringify(v,(_,x)=>typeof x==='bigint'?String(x):x,2)+'\n';
export async function deploy(client:GenLayerClient<typeof studionet>){
  if(client.chain?.id!==61999)throw Error('StudioNet 61999 required');
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
  async function deployOne(key:keyof Addresses,args:string[]){
    if(p.contracts[key])return p.contracts[key]!;
    const name='deploy-'+key;let hash=p.transactions[name];
    if(!hash){hash=await client.deployContract({code:readFileSync('contracts/'+key+'.py','utf8'),args}) as TransactionHash;p.transactions[name]=hash;save();console.log('Submitted '+name+' '+hash);}
    const receipt=await final(hash,name);p.contracts[key]=String(receipt.to_address??receipt.recipient) as `0x${string}`;save();return p.contracts[key]!;
  }
  async function write(name:string,address:`0x${string}`,method:string,args:Parameters<typeof client.writeContract>[0]['args'],value=0n){
    let hash=p.transactions[name];
    if(!hash){hash=await client.writeContract({address,functionName:method,args,value});p.transactions[name]=hash;save();console.log('Submitted '+name+' '+hash);}
    await final(hash,name);await descendants(hash,name);return hash;
  }
  async function reject(name:string,args:Parameters<typeof client.writeContract>[0]['args'],expected:string){
    let hash=p.transactions[name];
    if(!hash){hash=await client.writeContract({address:p.contracts.notes!,functionName:'create_note',args,value:0n});p.transactions[name]=hash;save();console.log('Submitted expected rejection '+name+' '+hash);}
    await client.waitForTransactionReceipt({hash,status:TransactionStatus.FINALIZED,retries:60,interval:5000});
    const raw=await rpc('eth_getTransactionByHash',[hash]);
    writeFileSync('docs/proofs/'+name+'.json',encode(raw));
    if(!raw||raw.status!=='FINALIZED'||finalized(raw)||!(encode(raw.consensus_data)+Buffer.from(String(((raw.consensus_data as {leader_receipt?:{result?:string}[]})?.leader_receipt?.[0]?.result)??''),'base64').toString()).includes(expected))throw Error('Unexpected rejection receipt '+encode(raw));
    p.rejections??={};p.rejections[name]=expected;save();console.log(name+' FINALIZED expected rejection '+hash+' leader: '+expected);
  }
  const step=process.env.FOOTNOTE_STEP??'deploy';
  if(step==='deploy'){
    const notes=await deployOne('notes',[JSON.stringify(['en.wikipedia.org','www.bbc.com','www.reuters.com','apnews.com','www.theguardian.com','www.nasa.gov','science.nasa.gov','svs.gsfc.nasa.gov','www.noaa.gov','www.ncei.noaa.gov','climate.copernicus.eu','www.gov.uk','www.justice.gov','europepmc.org','www.ebi.ac.uk'])]);
    const bonds=await deployOne('bonds',[notes]);
    const recheck=await deployOne('recheck',[notes]);
    const appeals=await deployOne('appeals',[notes,bonds]);
    await write('wire-bonds',bonds,'wire',[appeals]);await write('wire-notes',notes,'wire',[recheck,appeals,bonds]);
    p.states.config=JSON.parse(String(await read(notes,'get_config')));save();return;
  }
  if(!p.contracts.notes||!p.contracts.bonds||!p.contracts.appeals||!p.contracts.recheck)throw Error('Deploy all contracts first');
  const live=JSON.parse(readFileSync('docs/proofs/live-inputs.json','utf8'));
  const selected=process.env.FOOTNOTE_CASE??'supported';const input=live[selected];
  if(!input)throw Error('Unknown live case');
  const wallet=typeof client.account==='string'?client.account:client.account?.address;
  if(step==='reject-host')await reject('reject-host',['host-rejection',input.uri,JSON.stringify(['https://example.com/footnote-proof'])],'source host is not allowed');
  if(step==='reject-quota'){
    await reject('reject-quota',['climate-quota-4',input.uri,JSON.stringify(input.sources)],'three notes per post per address quota');
    p.states.quota={writer:wallet,uri:input.uri,value:JSON.parse(String(await read(p.contracts.notes,'get_quota',[wallet!,input.uri])))};save();
  }
  if(step==='recheck'){
    await write(selected+'-recheck',p.contracts.recheck,'recheck',[input.id,'[]']);
    p.states[input.id]=JSON.parse(String(await read(p.contracts.notes,'get_note',[input.id])));save();
    p.states.recheck=JSON.parse(String(await read(p.contracts.recheck,'get_operation',['recheck-1'])));save();
  }
  if(step==='stake'||step==='quota-note')await write(selected+'-stake',p.contracts.bonds,'stake',[input.id],2n*10n**18n);
  if(step==='note'||step==='quota-note'){
    if(!input.preflightPassed)throw Error('Three identical canonical fetches and exact quote check required');
    await write(selected+'-note',p.contracts.notes,'create_note',[input.id,input.uri,JSON.stringify(input.sources)]);
    const state=JSON.parse(String(await read(p.contracts.notes,'get_note',[input.id])));
    p.states[input.id]=state;save();
    if(state.status!=='active'||!input.expected.includes(state.history.at(-1).decision.evidence_label))throw Error('Unexpected live judgment '+encode(state));
  }
  if(step==='appeal'){
    await write(selected+'-contest',p.contracts.appeals,'contest',[input.id,1,JSON.stringify(input.counterSources??input.sources)],2n*10n**18n);
    await write(selected+'-judge',p.contracts.appeals,'judge',[input.id+':1']);
    await write(selected+'-settle',p.contracts.bonds,'settle_appeal',[input.id+':1']);
    p.states[input.id+':appeal']=JSON.parse(String(await read(p.contracts.appeals,'get_appeal',[input.id+':1'])));save();
  }
  if(step==='withdraw-deposit'){
    const claim='deposit:'+input.id+':1';
    if(!p.states[claim+':balances']){p.states[claim+':balances']={before:String(await client.getBalance({address:wallet!}))};save();}
    const hash=await write(selected+'-withdraw-deposit',p.contracts.bonds,'withdraw',[claim,1]);
    await write(selected+'-verify-deposit',p.contracts.bonds,'verify_claim',[claim,hash]);
    p.states[claim]=JSON.parse(String(await read(p.contracts.bonds,'get_claim',[claim])));
    p.states[claim+':balances']={...(p.states[claim+':balances'] as object),after:String(await client.getBalance({address:wallet!}))};save();
  }
  if(step==='withdraw-bond'){
    if(!p.transactions[selected+'-release']){const bond=JSON.parse(String(await read(p.contracts.bonds,'get_bond',[input.id])));if(Date.now()/1000<bond.deadline)throw Error('Bond is not mature; no write sent. Deadline UTC: '+new Date(bond.deadline*1000).toISOString());}
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
