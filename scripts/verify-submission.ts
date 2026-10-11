import {readFileSync,writeFileSync} from 'node:fs';
const p=JSON.parse(readFileSync('docs/submission/portal-fields.json','utf8'));
const limits:Record<string,number>={oneLiner:180,description:1000,expectedOutcome:500};
for(const [key,max] of Object.entries(limits)){console.log(key+': '+p[key].length+'/'+max);if(p[key].length>max)throw Error(key+' exceeds limit');}
if(!Array.isArray(p.howTo)||p.howTo.length!==4)throw Error('Exactly four how-to steps required');
const urls=[p.website,p.github,...Object.values(p.contractExplorerLinks),...p.evidenceLinks] as string[];
const results=[];
for(const url of urls){const response=await fetch(url,{redirect:'follow',signal:AbortSignal.timeout(30000)});results.push({url,status:response.status,finalUrl:response.url});console.log(response.status+' '+url);}
writeFileSync('docs/submission/link-check.json',JSON.stringify({checkedAt:new Date().toISOString(),results},null,2));
if(results.some(x=>x.status!==200))throw Error('Not every submission link returned HTTP 200');
