import test,{type TestContext} from 'node:test';
import assert from 'node:assert/strict';
import {connectWallet,walletErrorMessage} from '../lib/wallet';

const address='0x1111111111111111111111111111111111111111';
function install(t:TestContext,accounts:string[],permission:()=>Promise<unknown>){
  const previous=Object.getOwnPropertyDescriptor(globalThis,'window');
  const requests:string[]=[];
  Object.defineProperty(globalThis,'window',{configurable:true,value:{ethereum:{request:async({method}:{method:string})=>{
    requests.push(method);
    if(method==='eth_accounts')return accounts;
    if(method==='eth_requestAccounts')return permission();
    if(method==='eth_chainId')return '0xf22f';
    if(method==='wallet_getSnaps')return {genlayer:{id:'npm:genlayer-wallet-plugin'}};
    throw Error('Unexpected wallet method: '+method);
  }}}});
  t.after(()=>{if(previous)Object.defineProperty(globalThis,'window',previous);else Reflect.deleteProperty(globalThis,'window');});
  return requests;
}

test('ten concurrent connection attempts open one permission request and one plugin check',async t=>{
  let approve!:(value:string[])=>void;
  const permission=new Promise<string[]>(resolve=>{approve=resolve;});
  const requests=install(t,[],()=>permission);
  const attempts=Array.from({length:10},()=>connectWallet());
  await Promise.resolve();
  assert.equal(requests.filter(method=>method==='eth_requestAccounts').length,1);
  approve([address]);
  const sessions=await Promise.all(attempts);
  assert.ok(sessions.every(session=>session.address===address));
  assert.equal(requests.filter(method=>method==='wallet_getSnaps').length,1);
});

test('an authorized account reconnects without a new permission prompt',async t=>{
  const requests=install(t,[address],async()=>{throw Error('Permission prompt must not open.');});
  assert.equal((await connectWallet()).address,address);
  assert.ok(!requests.includes('eth_requestAccounts'));
});

test('a pending external request gives recovery instructions and does not poison the next attempt',async t=>{
  const accounts:string[]=[];
  install(t,accounts,async()=>{throw {code:-32002,message:"Request of type 'wallet_requestPermissions' already pending"};});
  await assert.rejects(connectWallet(),error=>{assert.match(walletErrorMessage(error),/Open your wallet extension and approve or cancel/);return true;});
  accounts.push(address);
  assert.equal((await connectWallet()).address,address);
});

test('a cancelled wallet request can be retried after approval',async t=>{
  let cancelled=true;
  install(t,[],async()=>{if(cancelled)throw {code:4001,message:'User rejected the request.'};return [address];});
  await assert.rejects(connectWallet(),error=>{assert.match(walletErrorMessage(error),/cancelled/);return true;});
  cancelled=false;
  assert.equal((await connectWallet()).address,address);
});
