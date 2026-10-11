import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {TransactionHashVariant} from 'genlayer-js/types';
export const RPC='https://studio.genlayer.com/api';
export const explorer='https://explorer-studio.genlayer.com';
export const readClient=()=>createClient({chain:studionet});
export async function rpc(method:string,params:unknown[]){
  const response=await fetch(RPC,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({jsonrpc:'2.0',id:1,method,params}),signal:AbortSignal.timeout(20000),cache:'no-store'});
  const data=await response.json();if(!response.ok||data.error)throw Error(data.error?.message??'StudioNet read unavailable.');return data.result as Record<string,unknown>|null;
}
export async function read(address:`0x${string}`,method:string,args:Parameters<ReturnType<typeof readClient>['readContract']>[0]['args']=[]){
  return readClient().readContract({address,functionName:method,args,transactionHashVariant:TransactionHashVariant.LATEST_FINAL});
}
