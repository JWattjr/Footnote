import {read} from '../lib/network';

let previousReadAt=0;
// StudioNet's standard bucket allows 30 gen_call reads/minute. Shared by all audit modules.
export async function verificationRead(...args:Parameters<typeof read>):Promise<Awaited<ReturnType<typeof read>>>{
  for(let attempt=0;;attempt++){
    const delay=Math.max(0,previousReadAt+2200-Date.now());
    if(delay)await new Promise(resolve=>setTimeout(resolve,delay));
    previousReadAt=Date.now();
    try{return await read(...args);}
    catch(error){
      if(attempt>=2)throw error;
      const issue=error as {cause?:{data?:{retry_after_seconds?:number}}};
      const seconds=Number(issue.cause?.data?.retry_after_seconds??2);
      const backoff=Math.min(60000,Math.max(3000,(seconds+1)*1000));
      console.log('Retrying the same read-only state check after '+backoff+'ms: '+args[1]);
      await new Promise(resolve=>setTimeout(resolve,backoff));
    }
  }
}
