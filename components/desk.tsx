'use client';
import Link from 'next/link';
import {useEffect,useState,useCallback,type FormEvent} from 'react';
import {ArrowUpRight,ArrowRight,BookOpen,Check,ChevronRight,ExternalLink,FileText,History,MessageSquare,RefreshCw,ShieldCheck,Wallet,X} from 'lucide-react';
import {evidenceLabels,evidenceText,toneText,sourceUrls,bondAmount,postLink,type Addresses,type Note,type Post,type Evidence} from '@/lib/domain';
import {explorer} from '@/lib/network';
type Feed={notes:Note[];posts:Record<string,Post>;addresses:Addresses;hosts:string[];unproven:string[]};
type Receipt={hash:`0x${string}`;action:string;status:string;target:string};
type Provider={request:(arg:{method:string;params?:unknown[]})=>Promise<unknown>};
async function connect(){
  const provider=(window as unknown as {ethereum?:Provider}).ethereum;
  if(!provider)throw Error('Enable a wallet with the GenLayer plugin to write. Reading is open to everyone.');
  const accounts=await provider.request({method:'eth_requestAccounts'}) as string[];
  if(!/^0x[a-fA-F0-9]{40}$/.test(accounts[0]??''))throw Error('Select a wallet account.');
  const [{createClient},{studionet}]=await Promise.all([import('genlayer-js'),import('genlayer-js/chains')]);
  const client=createClient({chain:studionet,account:accounts[0] as `0x${string}`,provider:provider as never});
  await client.connect('studionet');return {client,address:accounts[0]};
}
export default function Desk(){
  const [feed,setFeed]=useState<Feed>();const [error,setError]=useState('');const [loading,setLoading]=useState(true);
  const [selected,setSelected]=useState('');const [filter,setFilter]=useState<Evidence|'ALL'>('ALL');
  const [view,setView]=useState<'desk'|'write'|'proof'>('desk');const [version,setVersion]=useState<number>();
  const [wallet,setWallet]=useState('');const [busy,setBusy]=useState(false);const [receipt,setReceipt]=useState<Receipt>();
  const [id,setId]=useState('');const [uri,setUri]=useState('');const [sources,setSources]=useState('');const [stake,setStake]=useState('2');
  const [counter,setCounter]=useState('');const [bondReady,setBondReady]=useState('');const [withdrawHash,setWithdrawHash]=useState('');
  const [appealVersion,setAppealVersion]=useState('');
  const refresh=useCallback(async()=>{setLoading(true);try{const response=await fetch('/api/feed');const data=await response.json();if(!response.ok)throw Error(data.error);setFeed(data);setSelected(old=>old||data.notes[0]?.id||'');setError('');}catch(e){setError((e as Error).message);}finally{setLoading(false);}},[]);
  useEffect(()=>{const timer=setTimeout(()=>{void refresh();try{const saved=localStorage.getItem('footnote:receipt');if(saved)setReceipt(JSON.parse(saved));const bond=localStorage.getItem('footnote:bond');if(bond)setBondReady(bond);}catch{}},0);return()=>clearTimeout(timer);},[refresh]);
  const remember=(r:Receipt)=>{setReceipt(r);localStorage.setItem('footnote:receipt',JSON.stringify(r));};
  async function resume(r=receipt){if(!r)return;setBusy(true);setError('');try{
    for(let i=0;i<18;i++){const response=await fetch('/api/receipt?hash='+r.hash);const result=await response.json();if(!response.ok)throw Error(result.error??'Receipt unavailable.');
      if(result.status==='FAILED'){remember({...r,status:'Failed'});throw Error(result.error??'Finalized execution failed.');}
      remember({...r,status:result.done?'Finalized':result.status});if(result.done){if(r.action==='Stake bond'){setBondReady(r.target);localStorage.setItem('footnote:bond',r.target);}if(r.action.startsWith('Withdraw'))setWithdrawHash(r.hash);await refresh();return;}
      await new Promise(resolve=>setTimeout(resolve,4000));}
    setError('Still awaiting finality. Resume this transaction to check the same hash.');
  }catch(e){setError((e as Error).message);}finally{setBusy(false);}}
  async function write(action:string,contract:keyof Addresses,method:string,args:(string|number)[],value=0n,target=selected){
    if(receipt&&!['Finalized','Failed'].includes(receipt.status)){setError('Resume the pending transaction before making another write.');return;}
    setBusy(true);setError('');try{const address=feed?.addresses[contract];if(!address)throw Error('This contract is awaiting deployment.');
      const session=await connect();setWallet(session.address);const hash=await session.client.writeContract({address,functionName:method,args,value});
      const r:Receipt={hash,action,status:'Submitted',target};remember(r);setBusy(false);await resume(r);
    }catch(e){setError((e as Error).message);setBusy(false);}}
  async function create(event:FormEvent){event.preventDefault();try{
    if(!/^[a-z0-9-]{1,64}$/.test(id))throw Error('Use a note ID with lowercase letters, numbers, and dashes.');
    if(!postLink(uri))throw Error('Paste the post AT URI with its DID, rather than its profile link.');
    const urls=sourceUrls(sources,feed?.hosts??[]);
    if(bondReady!==id){await write('Stake bond','bonds','stake',[id],bondAmount(stake),id);return;}
    await write('Publish note','notes','create_note',[id,uri,JSON.stringify(urls)],0n,id);setSelected(id);setView('desk');
  }catch(e){setError((e as Error).message);}}
  const notes=feed?.notes.filter(n=>filter==='ALL'||n.history.at(-1)?.decision.evidence_label===filter)??[];
  const note=feed?.notes.find(n=>n.id===selected);const entry=note?.history.find(v=>v.version===(version??note.version))??note?.history.at(-1);
  const decision=entry?.decision;const post=note&&feed?.posts[note.post_uri];
  const displayedSources=decision?.sources??(entry?.version===note?.version?note?.sources:[...new Set([...Object.keys(decision?.source_digests??{}),...(decision?.citations.map(c=>c.url)??[])])])??[];
  const canAct=!!note&&note.status==='active'&&!busy;const appealId=note?note.id+':'+(appealVersion||note.version):'';
  const canManage=!!note&&!busy;
  function counterSources(){return counter.trim()?sourceUrls(counter,feed?.hosts??[]):[];}
  async function action(action:string){if(!note)return;try{
    const sources=['Recheck sources','Contest note'].includes(action)?JSON.stringify(counterSources()):'[]';
    if(action==='Recheck sources')await write(action,'recheck','recheck',[note.id,sources]);
    if(action==='Fund appeal')await write(action,'bonds','fund_appeal',[note.id,note.version],2n*10n**18n);
    if(action==='Contest note')await write(action,'appeals','contest',[note.id,note.version,sources]);
    if(action==='Judge appeal')await write(action,'appeals','judge',[appealId]);
    if(action==='Settle appeal')await write(action,'bonds','settle_appeal',[appealId]);
    if(action==='Cancel stale appeal')await write(action,'appeals','cancel_stale',[appealId]);
    if(action==='Resume appeal')await write(action,'appeals','resume_appeal',[appealId]);
    if(action==='Resume deposit')await write(action,'bonds','resume_deposit',[appealId]);
    if(action==='Resume bond')await write(action,'bonds','resume_bond',[note.id]);
    if(action==='Resume note')await write(action,'notes','resume_note',[note.id]);
    if(action==='Resume bond verification')await write(action,'bonds','resume_claim',['bond:'+note.id]);
    if(action==='Resume deposit verification')await write(action,'bonds','resume_claim',['deposit:'+appealId]);
    if(['Refund unused funding','Resume funding','Withdraw unused funding','Verify funding withdrawal','Resume funding verification'].includes(action)){
      const session=await connect();setWallet(session.address);
      const funding=appealId+':'+session.address.toLowerCase();const claim='funding:'+funding;
      if(action==='Refund unused funding')await write(action,'bonds','refund_unopened',[funding]);
      if(action==='Resume funding')await write(action,'bonds','resume_funding',[funding]);
      if(action==='Verify funding withdrawal')await write(action,'bonds','verify_claim',[claim,withdrawHash]);
      if(action==='Resume funding verification')await write(action,'bonds','resume_claim',[claim]);
      if(action==='Withdraw unused funding'){
        const response=await fetch('/api/claim?claim='+encodeURIComponent(claim));const state=await response.json();
        if(!response.ok)throw Error(state.error);
        if(!['available','failed'].includes(state.status))throw Error('Claim is '+state.status+'. Verify the pending receipt before retrying.');
        await write(action,'bonds','withdraw',[claim,state.attempt+1]);
      }
    }
    if(action==='Release bond')await write(action,'bonds','release',[note.id]);
    if(action==='Withdraw deposit'||action==='Withdraw bond'){
      const claim=action==='Withdraw deposit'?'deposit:'+appealId:'bond:'+note.id;
      const response=await fetch('/api/claim?claim='+encodeURIComponent(claim));const state=await response.json();
      if(!response.ok)throw Error(state.error);
      if(!['available','failed'].includes(state.status))throw Error('Claim is '+state.status+'. Verify the pending receipt before retrying.');
      await write(action,'bonds','withdraw',[claim,state.attempt+1]);
    }
    if(action==='Verify deposit withdrawal')await write(action,'bonds','verify_claim',['deposit:'+appealId,withdrawHash]);
    if(action==='Verify bond withdrawal')await write(action,'bonds','verify_claim',['bond:'+note.id,withdrawHash]);
  }catch(e){setError((e as Error).message);}}
  return <div className="shell">
    <a href="#content" className="skip">Skip to notes</a>
    <header className="masthead"><button className="brand" onClick={()=>setView('desk')} aria-label="Footnote home">footnote<span className="brand-mark">*</span></button>
      <nav aria-label="Main"><button className={view==='desk'?'current':''} onClick={()=>setView('desk')}>Evidence desk</button><button className={view==='proof'?'current':''} onClick={()=>setView('proof')}>Live proof <ArrowUpRight size={14}/></button></nav>
      <button className="wallet" disabled={busy} onClick={async()=>{try{const s=await connect();setWallet(s.address);setError('');}catch(e){setError((e as Error).message);}}}><Wallet size={16}/>{wallet?wallet.slice(0,6)+'…'+wallet.slice(-4):'Connect wallet'}</button>
    </header>
    <main id="content">
      <div className="intro"><div><h1>Follow the evidence.</h1><p>A little context. A clearer conversation.</p></div><button className="primary" onClick={()=>{setView('write');setError('');}}><FileText size={16}/> Write a note <ArrowRight size={16}/></button></div>
      <div className="network-strip"><span><span className="network-dot"/> GenLayer StudioNet</span><span>Public demo: 15-minute appeal window · production default: 72 hours</span><button disabled={loading||busy} onClick={()=>void refresh()}><RefreshCw size={13} className={loading?'spin':''}/>Refresh</button></div>
      {error&&<div className="error" role="alert"><span>{error}</span><button aria-label="Dismiss error" onClick={()=>setError('')}><X size={16}/></button></div>}
      {receipt&&<div className="receipt" role="status"><span>{receipt.action}: <strong>{receipt.status}</strong></span><a href={explorer+'/transactions/'+receipt.hash} target="_blank" rel="noreferrer">View transaction <ExternalLink size={12}/></a>{!['Finalized','Failed'].includes(receipt.status)&&<button disabled={busy} onClick={()=>void resume()}>Resume transaction</button>}</div>}
      {view==='write'?<section className="write-page"><button className="text-button" onClick={()=>setView('desk')}>Back to notes</button><h2>Add context to a public post.</h2><p>Validators read the post and your sources. Evidence and tone receive separate labels. The public demo locks your bond for 15 minutes and until any appeal closes. The production default is 72 hours.</p>
        <form onSubmit={create}><label>Note ID<input required value={id} onChange={e=>setId(e.target.value)} placeholder="your-note-id" maxLength={64}/></label><label>Bluesky post AT URI<input required value={uri} onChange={e=>setUri(e.target.value)} placeholder="at://did:plc:…/app.bsky.feed.post/…"/></label>
          <label>Source URLs<textarea required value={sources} onChange={e=>setSources(e.target.value)} placeholder="One HTTPS source per line" rows={4}/></label><details><summary>Allowed source hosts</summary><p className="hosts">{feed?.hosts.join(', ')||'Available after deployment.'}</p></details>
          <label>Writer bond (simulated GEN)<input type="number" min={2} max={20} step={1} value={stake} onChange={e=>setStake(e.target.value)}/></label><button className="primary" disabled={busy||!feed?.addresses.notes}>{busy?'Waiting for finality…':bondReady===id?'Publish note':'Stake bond'}<ArrowRight size={16}/></button>
          <p className="small">Two steps: finalize your bond, then publish your note. No post text or Bluesky handle is stored on-chain.</p></form></section>
      :view==='proof'?<section className="proof-page"><h2>Proof you can inspect.</h2><p>Every contract and transaction opens in the explorer. Finality alone does not prove successful execution, and a reserved withdrawal does not prove native credit.</p>
        <div className="contract-list">{Object.entries(feed?.addresses??{}).map(([name,address])=><a key={name} href={explorer+'/contracts/'+address} target="_blank" rel="noreferrer"><strong>{name}</strong><code>{address}</code><ArrowUpRight size={16}/></a>)}</div>
        <p><Link href="/replay">Watch the test-only source-change replay <ArrowRight size={14}/></Link></p><h3>Live proof limits</h3><ul>{feed?.unproven.map(item=><li key={item}>{item}</li>)}</ul><a href="/deployment.json" target="_blank" rel="noreferrer">Download the live proof manifest <ArrowUpRight size={14}/></a><p><a href="https://github.com/JWattjr/Footnote/tree/main/docs">Architecture, tests, and tutorial</a></p></section>
      :<div className="desk-grid"><aside className="index"><div className="index-title"><h2>Community notes</h2><span>{feed?.notes.length??0}</span></div><label className="mobile-note-picker">Note<select value={selected} onChange={e=>{setSelected(e.target.value);setVersion(undefined);setCounter('');setAppealVersion('');}}>{(feed?.notes??[]).map(n=><option key={n.id} value={n.id}>{n.id} · {n.history.at(-1)?.decision.evidence_label.toLowerCase()}</option>)}</select></label><label className="filter">Evidence<select value={filter} onChange={e=>setFilter(e.target.value as Evidence|'ALL')}><option value="ALL">All labels</option>{evidenceLabels.map(l=><option key={l} value={l}>{l[0]+l.slice(1).toLowerCase()}</option>)}</select></label>
        <div className="note-index">{notes.map(n=>{const d=n.history.at(-1)?.decision;return <button key={n.id} className={selected===n.id?'selected':''} onClick={()=>{setSelected(n.id);setVersion(undefined);setCounter('');setAppealVersion('');}}><span className={'mini-label '+d?.evidence_label.toLowerCase()}>{d?evidenceText(d):'Awaiting finality'}</span><strong>{feed?.posts[n.post_uri]?.record.text??'Post unavailable'}</strong><span className="index-meta">v{n.version} · {n.sources.length} source{n.sources.length===1?'':'s'}<ChevronRight size={14}/></span></button>;})}</div>
        {!notes.length&&<p className="empty-index">{loading?'Reading finalized notes…':'No notes match this view.'}</p>}<div className="index-note"><ShieldCheck size={18}/><p>Judged from sources.<br/>Open to challenge.</p></div></aside>
        <article className="case-file">{note&&decision?<><div className="case-top"><span>Note / {note.id}</span><span>Version {entry?.version} of {note.version}</span></div>
          <section className="post"><div className="post-byline"><span className="avatar"><MessageSquare size={18}/></span><div><strong>{post?.author.displayName||'Public Bluesky post'}</strong><span>{post?'@'+post.author.handle:'Post unavailable'}</span></div><a aria-label="Open original Bluesky post" href={postLink(note.post_uri)} target="_blank" rel="noreferrer"><ArrowUpRight size={20}/></a></div><p className="post-text">{post?.record.text??'This post is unavailable. Its fingerprint and note history are preserved.'}</p><div className="post-meta"><span>{post?new Date(post.record.createdAt).toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'}):'Original post unavailable'}</span><span>{post?.repostCount??0} reposts · {post?.likeCount??0} likes</span></div></section>
          <section className="judgment"><div className="judgment-heading"><BookOpen size={19}/><h2>The footnote</h2><span>{note.status==='active'?<><Check size={13}/>Finalized</>:'Awaiting finality'}</span></div><div className="label-pair"><div className={'evidence-label '+decision.evidence_label.toLowerCase()}><span>Evidence</span><strong>{evidenceText(decision)}</strong></div><div className="tone-label"><span>Tone · judged separately</span><strong>{toneText(decision.tone_label)}</strong></div></div>
            <p className="judgment-copy">{decision.IS_ALLEGATION_ABOUT_PERSON==='yes'?'This note describes available public reporting. It makes no finding about guilt or innocence.':decision.evidence_label==='UNSUPPORTED'?'The supplied sources do not establish this claim either way. This is a valid outcome; new evidence can change it.':decision.evidence_label==='SUPPORTED'?'The cited sources explicitly support the factual claim. Read the quoted evidence below.':decision.evidence_label==='CONTRADICTED'?'The cited sources say otherwise. The exact passages below show what validators relied on.':'The cited facts do not establish what the post implies. Read the sources in context.'}</p>
            {!decision.post_available&&<p className="unavailable">Post unavailable or changed. Previous versions remain below.</p>}
          </section>
          <section className="source-section"><h3>The sources <span>{displayedSources.length}</span></h3>{displayedSources.map((url,i)=>{const cite=decision.citations.find(c=>c.url===url);return <div className="source" key={url}><span className="source-number">[{i+1}]</span><div><a href={url} target="_blank" rel="noreferrer">{new URL(url).hostname}<ArrowUpRight size={14}/></a>{cite?.quote?<blockquote>“{cite.quote}”</blockquote>:<p>{cite?.quote_sha256?'Exact quote verified; withheld from on-chain storage for person safety.':'Supplied source; no supporting quote established for this label.'}</p>}<span className="digest">{decision.source_digests[url]?'Canonical digest '+decision.source_digests[url].slice(0,16)+'…':'Source unavailable at judgment'}</span></div></div>;})}</section>
          <section className="history-section"><h3><History size={17}/> Follow the changes</h3><p>Every version stays in the record. Select one to read its evidence.</p><div className="history-list">{note.history.map(v=><button key={v.version} aria-pressed={entry?.version===v.version} onClick={()=>setVersion(v.version)}><span className="history-node"/><strong>v{v.version}</strong><span>{evidenceText(v.decision)}</span><small>{v.reason==='CREATED'?'Note published':v.reason==='APPEAL'?'Appeal judgment':'Sources rechecked'}</small><span>{new Date(v.at*1000).toLocaleDateString('en-GB',{day:'numeric',month:'short'})}</span></button>)}</div>{note.history.length===1&&<p className="small">No live label change recorded for this note.</p>}</section>
          <details className="action-panel"><summary>Recheck or challenge this note <ChevronRight size={16}/></summary><div><label>New evidence URLs (optional)<textarea value={counter} onChange={e=>setCounter(e.target.value)} rows={3} placeholder="Add an allowed source or a published correction"/></label><div className="actions"><button disabled={!canAct} onClick={()=>void action('Recheck sources')}><RefreshCw size={15}/>Recheck sources</button><button disabled={!canAct} onClick={()=>void action('Fund appeal')}>Fund appeal · 2 GEN</button><button disabled={!canAct} onClick={()=>void action('Contest note')}>Contest note</button></div><p className="small">Appeals close {new Date(note.deadline*1000).toLocaleString('en-GB')}. First fund the deposit directly in Bonds, then contest after funding finalizes. One appeal per version. A cancelled or uncertain appeal refunds the deposit. Rechecks wait until the appeal closes.</p><div className="actions"><button disabled={!canAct} onClick={()=>void action('Judge appeal')}>Judge appeal</button><button disabled={!canAct} onClick={()=>void action('Settle appeal')}>Settle appeal</button></div></div></details>
          <details className="action-panel"><summary>Bonds and withdrawals <Wallet size={16}/></summary><div><label>Existing appeal version<input type="number" min={1} max={note.version} value={appealVersion||String(note.version)} onChange={e=>setAppealVersion(e.target.value)}/></label><p className="small">Use the original appealed version for judging, cancellation, settlement and deposit withdrawals.</p><p>Writer bond: 2–20 simulated GEN. Withdraw only after settlement. Native credit is verified separately.</p><div className="actions">{['Release bond','Withdraw bond','Withdraw deposit','Cancel stale appeal','Resume appeal','Resume deposit','Resume bond','Resume note','Resume bond verification','Resume deposit verification','Refund unused funding','Resume funding','Withdraw unused funding','Resume funding verification'].map(a=><button key={a} disabled={!canManage} onClick={()=>void action(a)}>{a}</button>)}</div><label>Withdrawal transaction hash<input value={withdrawHash} onChange={e=>setWithdrawHash(e.target.value)} placeholder="0x…"/></label><div className="actions">{['Verify bond withdrawal','Verify deposit withdrawal','Verify funding withdrawal'].map(a=><button key={a} disabled={!canManage||!/^0x[a-fA-F0-9]{64}$/.test(withdrawHash)} onClick={()=>void action(a)}>{a}</button>)}</div><p className="small">Failed credit recovery uses the next attempt after receipt verification. Inspect the claim via the contract explorer before retrying.</p></div></details>
        </>:<div className="empty-case"><BookOpen size={32}/><h2>{loading?'Opening the evidence desk…':'The next post needs context.'}</h2><p>{loading?'Reading finalized contract state and the public Bluesky post.':'Published notes will appear here with source quotes and a permanent version history.'}</p><button className="primary" onClick={()=>setView('write')}>Write a note <ArrowRight size={16}/></button></div>}</article>
        <aside className="margin"><h3>Context matters.</h3><p>True can still be provocative. Unsupported can still be useful. Evidence and tone answer different questions.</p><hr/><h4>Four labels, one record.</h4><dl><dt>Supported</dt><dd>Sources state the claim.</dd><dt>Contradicted</dt><dd>Sources say otherwise.</dd><dt>Unsupported</dt><dd>No credible source either way.</dd><dt>Misleading</dt><dd>Facts imply more than they show.</dd></dl><hr/><p className="small">Allegations about people use a stricter rule: Supported or “No credible public source found yet.”</p><a href="https://github.com/JWattjr/Footnote/blob/main/docs/SECURITY_NOTES.md">Read the safety rules <ArrowUpRight size={13}/></a></aside>
      </div>}
    </main><footer><span className="footer-brand">footnote*</span><p>Labels are judgments about sources, not truth. Bluesky only. StudioNet is a simulator.</p><a href="https://github.com/JWattjr/Footnote">GitHub <ArrowUpRight size={13}/></a></footer>
  </div>;
}
