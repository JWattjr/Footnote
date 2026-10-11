import {rpc} from '@/lib/network';
import {finalized} from '@/lib/domain';
export async function GET(request:Request){
  const hash=new URL(request.url).searchParams.get('hash');
  if(!hash||!/^0x[a-fA-F0-9]{64}$/.test(hash))return Response.json({error:'Invalid transaction hash.'},{status:400});
  try{
    const root=await rpc('eth_getTransactionByHash',[hash]);
    if(!root)return Response.json({status:'PENDING',done:false});
    let done=root.status==='FINALIZED';const checked:unknown[]=[];
    async function children(tx:Record<string,unknown>,depth:number){
      if(depth>5)throw Error('Callback depth exceeded. Inspect the explorer.');
      for(const id of (tx.triggered_transactions??[]) as string[]){const child=await rpc('eth_getTransactionByHash',[id]);
        if(!child||child.status!=='FINALIZED'){done=false;continue;}
        if(child.type===0&&child.consensus_data===null){if(child.value_credited!==true)throw Error('Native credit failed; verify the claim before retrying.');}
        else if(!finalized(child))throw Error('Finalized callback failed. Inspect the explorer before retrying.');
        checked.push({hash:id,native_credit:child.value_credited});await children(child,depth+1);}
    }
    if(done){if(!finalized(root))return Response.json({status:'FAILED',done:true,error:'Finalized execution failed. Inspect the explorer receipt.'});await children(root,0);}
    return Response.json({status:root.status,done,children:checked});
  }catch(e){return Response.json({error:e instanceof Error?e.message:'Receipt read failed.'},{status:503});}
}
