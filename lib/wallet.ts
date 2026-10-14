type Provider={request:(arg:{method:string;params?:unknown[]})=>Promise<unknown>};

async function requestConnection(){
  const provider=(window as unknown as {ethereum?:Provider}).ethereum;
  if(!provider)throw Error('Enable MetaMask with the GenLayer plugin to write. Reading is open to everyone.');
  // Reuse permission already granted to this site without opening another prompt.
  let accounts=await provider.request({method:'eth_accounts'}) as string[];
  if(!Array.isArray(accounts)||!accounts.length)accounts=await provider.request({method:'eth_requestAccounts'}) as string[];
  if(!Array.isArray(accounts)||!/^0x[a-fA-F0-9]{40}$/.test(accounts[0]??''))throw Error('Select a wallet account.');
  const [{createClient},{studionet}]=await Promise.all([import('genlayer-js'),import('genlayer-js/chains')]);
  const client=createClient({chain:studionet,account:accounts[0] as `0x${string}`,provider:provider as never});
  await client.connect('studionet');
  return {client,address:accounts[0]};
}

let pending:ReturnType<typeof requestConnection>|undefined;
export function connectWallet(){
  // Multiple gestures share one permission/network/plugin request, including failures.
  pending??=requestConnection().finally(()=>{pending=undefined;});
  return pending;
}

export function walletErrorMessage(error:unknown){
  const issue=error as {code?:number;message?:string;cause?:{code?:number};data?:{originalError?:{code?:number}}}|null;
  const code=issue?.code??issue?.cause?.code??issue?.data?.originalError?.code;
  const message=issue?.message??String(error);
  if(code===-32002||/already pending|request.*pending/i.test(message))return 'Your wallet already has a request waiting. Open your wallet extension and approve or cancel it, then try connecting again.';
  if(code===4001)return 'Wallet request cancelled. You can try again when you are ready.';
  return message;
}
