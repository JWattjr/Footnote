export const evidenceLabels = ['SUPPORTED','CONTRADICTED','UNSUPPORTED','MISLEADING'] as const;
export type Evidence = typeof evidenceLabels[number];
export type Tone = 'RAGE_BAIT'|'NOT_RAGE_BAIT'|'UNCLEAR';
export type Decision = {evidence_label:Evidence;tone_label:Tone;IS_ALLEGATION_ABOUT_PERSON:'yes'|'no';citations:{url:string;quote?:string;quote_sha256?:string}[];source_digests:Record<string,string>;post_available:boolean;fingerprint:string;sources?:string[]};
export type Version = {version:number;at:number;reason:string;operation:string;decision:Decision};
export type Note = {id:string;writer:string;post_uri:string;fingerprint:string;sources:string[];created_at:number;deadline:number;status:string;version:number;history:Version[];open:boolean};
export type Post = {uri:string;text:string;author:{displayName?:string;handle:string};likeCount?:number;repostCount?:number;record:{text:string;createdAt:string}};
export type Addresses = {notes?:`0x${string}`;recheck?:`0x${string}`;bonds?:`0x${string}`;appeals?:`0x${string}`};
export const evidenceText = (d:Decision) => d.IS_ALLEGATION_ABOUT_PERSON==='yes' && d.evidence_label==='UNSUPPORTED' ? 'No credible public source found yet' : ({SUPPORTED:'Supported',CONTRADICTED:'Contradicted',UNSUPPORTED:'Unsupported',MISLEADING:'Misleading'}[d.evidence_label]);
export const toneText = (tone:Tone) => ({RAGE_BAIT:'Rage bait',NOT_RAGE_BAIT:'Not rage bait',UNCLEAR:'Tone unclear'}[tone]);
export function sourceUrls(text:string, hosts:string[]):string[]{
  const urls=[...new Set(text.split(/\s+/).filter(Boolean))];
  if(!urls.length || urls.length>8) throw Error('Add one to eight HTTPS source URLs.');
  for(const url of urls){let parsed:URL;try{parsed=new URL(url);}catch{throw Error('A source URL is invalid.');}
    if(parsed.protocol!=='https:'||!hosts.includes(parsed.hostname)||parsed.username||parsed.password||parsed.hash||(parsed.port&&parsed.port!=='443'))throw Error('Source host is not allowed: '+parsed.hostname);
  }return urls.sort();
}
export function bondAmount(text:string):bigint{if(!/^(?:[2-9]|1\d|20)$/.test(text))throw Error('Choose a writer bond from 2 to 20 GEN.');return BigInt(text)*10n**18n;}
export function postLink(uri:string){const match=/^at:\/\/(did:plc:[a-z2-7]{24})\/app\.bsky\.feed\.post\/([a-zA-Z0-9]+)$/.exec(uri);return match?`https://bsky.app/profile/${match[1]}/post/${match[2]}`:undefined;}
export function finalized(receipt:Record<string,unknown>){
  const consensus=receipt.consensus_data as {leader_receipt?:{execution_result?:string;result?:{status?:string}}[]}|null|undefined;
  const leader=consensus?.leader_receipt?.[0];
  return (receipt.status??receipt.statusName??receipt.status_name)==='FINALIZED'&&receipt.result===6&&['SUCCESS','FINISHED_WITH_RETURN'].includes(String(receipt.txExecutionResultName??leader?.execution_result))&&leader?.result?.status!=='rollback';
}
