import deployment from '@/public/deployment.json';
import type {Addresses} from '@/lib/domain';
import {read} from '@/lib/network';
export async function GET(request:Request){
  const id=new URL(request.url).searchParams.get('claim');
  if(!id||!/^(bond:[a-z0-9-]{1,64}|deposit:[a-z0-9-]{1,64}:\d+)$/.test(id))return Response.json({error:'Invalid claim ID.'},{status:400});
  const bonds=(deployment.contracts as Addresses).bonds;if(!bonds)return Response.json({error:'Bonds is awaiting deployment.'},{status:503});
  try{return Response.json(JSON.parse(String(await read(bonds,'get_claim',[id]))));}
  catch(e){return Response.json({error:e instanceof Error?e.message:'Claim unavailable.'},{status:409});}
}
