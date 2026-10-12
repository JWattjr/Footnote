import {readFileSync} from 'node:fs';
import {finalized,type Addresses} from '../lib/domain';
import {rpc,read,readClient} from '../lib/network';
const p=JSON.parse(readFileSync('public/deployment.json','utf8')) as {contracts:Addresses;transactions:Record<string,string>;states:Record<string,unknown>;rejections?:Record<string,string>;accounting?:{wallet:`0x${string}`;walletBalance:string;bondsBalance:string;totals:{received:string;paid:string}}};
if(Object.keys(p.contracts).length!==4)throw Error('Four deployed contracts required');
const allHashes=new Set(Object.values(p.transactions));
for(const [name,hash] of Object.entries(p.transactions)){
  const receipt=await rpc('eth_getTransactionByHash',[hash]);
  if(!receipt)throw Error(name+' missing receipt');
  if(p.rejections?.[name]){
    if(receipt.status!=='FINALIZED'||finalized(receipt)||!(JSON.stringify(receipt.consensus_data)+Buffer.from(String(((receipt.consensus_data as {leader_receipt?:{result?:string}[]})?.leader_receipt?.[0]?.result)??''),'base64').toString()).includes(p.rejections[name]))throw Error(name+' expected rejection differs');
    const leaders=(receipt.consensus_data as {leader_receipt:{result?:string;execution_stats?:{call_counts?:Record<string,number>}}[]}).leader_receipt;
    // StudioNet can append a literal protocol idle placeholder with no execution stats.
    const executed=leaders.filter(leader=>!Buffer.from(leader.result??'','base64').equals(Buffer.from([2,105,100,108,101])));
    if(!executed.length)throw Error(name+' has no executed rejection trace');
    for(const leader of executed){const calls=leader.execution_stats?.call_counts;if(!calls||Object.keys(calls).some(k=>!['STORAGE_READ','NOTIFY_FINISHED'].includes(k)))throw Error(name+' pre-fetch execution trace differs');}
  }
  else if(receipt.type===0&&receipt.consensus_data===null){if(receipt.status!=='FINALIZED'||receipt.value_credited!==true)throw Error(name+' lacks native credit');}
  else if(!finalized(receipt))throw Error(name+' not finalized successfully');
  for(const child of (receipt.triggered_transactions??[]) as string[])if(!allHashes.has(child))throw Error(name+' has an undocumented child '+child);
  if(name.startsWith('deploy-')){const code=(receipt.data as {contract_code:string}).contract_code;if(!Buffer.from(code,'base64').equals(readFileSync('contracts/'+name.slice(7)+'.py')))throw Error(name+' source bytes differ');}
  console.log(name+' verified '+hash);
}
for(const [key,expected] of Object.entries(p.states)){
  let actual:unknown;
  if(key==='quota'){const q=expected as {writer:string;uri:string;value:unknown};actual={writer:q.writer,uri:q.uri,value:JSON.parse(String(await read(p.contracts.notes!,'get_quota',[q.writer,q.uri])))};}
  else if(key==='recheck')actual=JSON.parse(String(await read(p.contracts.recheck!,'get_operation',['recheck-1'])));
  else if(key==='config')actual=JSON.parse(String(await read(p.contracts.notes!,'get_config')));
  else if(key==='bondsConfig')actual=JSON.parse(String(await read(p.contracts.bonds!,'get_config')));
  else if(key==='appealsConfig')actual=JSON.parse(String(await read(p.contracts.appeals!,'get_config')));
  else if(key.startsWith('escrowBond:'))actual=JSON.parse(String(await read(p.contracts.bonds!,'get_bond',[key.slice(11)])));
  else if(key.startsWith('escrowDeposit:'))actual=JSON.parse(String(await read(p.contracts.bonds!,'get_deposit',[key.slice(14)])));
  else if(key.startsWith('fundingRecord:'))actual=JSON.parse(String(await read(p.contracts.bonds!,'get_funding',[key.slice(14)])));
  else if(key.startsWith('bond:')||key.startsWith('deposit:')){if(key.endsWith(':balances')){const balance=expected as {before:string;after:string};const claim=p.states[key.slice(0,-9)] as {amount:string};if(BigInt(balance.after)-BigInt(balance.before)!==BigInt(claim.amount))throw Error(key+' exact balance delta differs');console.log(key+' exact balance delta '+claim.amount+' wei');continue;}actual=JSON.parse(String(await read(p.contracts.bonds!,'get_claim',[key])));}
  else if(key.endsWith(':appeal'))actual=JSON.parse(String(await read(p.contracts.appeals!,'get_appeal',[key.slice(0,-7)+':1'])));
  else actual=JSON.parse(String(await read(p.contracts.notes!,'get_note',[key])));
  if(JSON.stringify(actual)!==JSON.stringify(expected))throw Error(key+' state differs from manifest; inspect legitimate later versions');
  console.log(key+' final state matches');
}
if(p.accounting){
  const totals=JSON.parse(String(await read(p.contracts.bonds!,'get_totals')));
  const client=readClient();
  const bondsBalance=String(await client.getBalance({address:p.contracts.bonds!}));
  const walletBalance=String(await client.getBalance({address:p.accounting.wallet}));
  if(JSON.stringify(totals)!==JSON.stringify(p.accounting.totals)||bondsBalance!==p.accounting.bondsBalance||walletBalance!==p.accounting.walletBalance||BigInt(bondsBalance)!==BigInt(totals.received)-BigInt(totals.paid))throw Error('Exact final escrow accounting differs');
  console.log('Wallet and Bonds exact balances and verified-paid totals match');
}
console.log('Read-only verification complete.');
