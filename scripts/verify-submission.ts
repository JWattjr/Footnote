import {readFileSync,writeFileSync} from 'node:fs';
const p=JSON.parse(readFileSync('docs/submission/portal-fields.json','utf8'));
const deployment=JSON.parse(readFileSync('public/deployment.json','utf8'));
const packageFiles=['README.md','docs/SECURITY_NOTES.md','docs/TEST_MATRIX.md','docs/PROOF_MANIFEST.md'];
const packageLinks=packageFiles.flatMap(file=>Array.from(readFileSync(file,'utf8').matchAll(/\]\((https?:\/\/[^\s)]+)\)/g),match=>match[1]));
const recoveryHashes=(deployment.legacyCleanup??[]).flatMap((file:string)=>Object.values(JSON.parse(readFileSync(file,'utf8')).transactions)) as string[];
for(const file of packageFiles){
  const contents=readFileSync(file,'utf8');
  for(const address of Object.values(deployment.contracts) as string[])if(!contents.includes(address))throw Error(file+' lacks current address '+address);
}
const limits:Record<string,number>={oneLiner:180,description:1000,expectedOutcome:500};
for(const [key,max] of Object.entries(limits)){console.log(key+': '+p[key].length+'/'+max);if(p[key].length>max)throw Error(key+' exceeds limit');}
if(!Array.isArray(p.howTo)||p.howTo.length!==4)throw Error('Exactly four how-to steps required');
const urls=[...new Set([p.website,p.github,...Object.values(p.contractExplorerLinks),...p.evidenceLinks,...packageLinks,...[...Object.values(deployment.transactions),...recoveryHashes].map(hash=>'https://explorer-studio.genlayer.com/transactions/'+hash)])] as string[];
const results=[];
for(let offset=0;offset<urls.length;offset+=2){
  results.push(...await Promise.all(urls.slice(offset,offset+2).map(async url=>{
    const attempts:number[]=[];let response:Response;
    for(let attempt=0;;attempt++){
      response=await fetch(url,{redirect:'follow',headers:{'User-Agent':'Footnote-link-check/2.0'},signal:AbortSignal.timeout(30000)});attempts.push(response.status);
      if(attempt>=1||(response.status!==429&&response.status<500))break;
      await new Promise(resolve=>setTimeout(resolve,1000));
    }
    return {url,status:response.status,finalUrl:response.url,attempts};
  })));
}
for(const result of results)console.log(result.status+' '+result.url);
writeFileSync('docs/submission/link-check.json',JSON.stringify({checkedAt:new Date().toISOString(),results},null,2));
if(results.some(x=>x.status!==200))throw Error('Not every submission link returned HTTP 200');
