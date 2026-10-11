import deployment from '@/public/deployment.json';
import {read} from '@/lib/network';
import type {Addresses,Note,Post} from '@/lib/domain';
import {createHash} from 'node:crypto';
export async function GET(){
  try{
    const addresses=deployment.contracts as Addresses;
    if(!addresses.notes)return Response.json({notes:[],posts:{},addresses,hosts:[],unproven:deployment.unproven});
    const [configRaw,idsRaw]=await Promise.all([read(addresses.notes,'get_config'),read(addresses.notes,'list_notes',[0,12])]);
    const config=JSON.parse(String(configRaw));
    const notes=await Promise.all((idsRaw as string[]).map(async id=>JSON.parse(String(await read(addresses.notes!,'get_note',[id]))) as Note));
    const uris=[...new Set(notes.map(n=>n.post_uri))];
    const posts:Record<string,Post>={};
    if(uris.length){const query=uris.map(uri=>'uris='+encodeURIComponent(uri)).join('&');
      const response=await fetch('https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts?'+query,{next:{revalidate:30},signal:AbortSignal.timeout(15000)});
      if(response.ok){const data=await response.json();for(const p of data.posts??[]){const matches=notes.filter(n=>n.post_uri===p.uri);
        const hash=createHash('sha256').update(p.record.text).digest('hex');
        if(matches.every(n=>n.fingerprint===hash))posts[p.uri]={...p,text:p.record.text};}}}
    return Response.json({notes,posts,addresses,hosts:config.hosts,unproven:deployment.unproven},{headers:{'Cache-Control':'public, s-maxage=30, stale-while-revalidate=60'}});
  }catch(e){return Response.json({error:e instanceof Error?e.message:'Network read failed.'},{status:503});}
}
