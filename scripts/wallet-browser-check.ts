import {chromium,expect} from '@playwright/test';
import {mkdirSync,readFileSync,writeFileSync} from 'node:fs';

const url=process.env.FOOTNOTE_URL??'http://localhost:3118';
const deployment=JSON.parse(readFileSync('public/deployment.json','utf8'));
const folder='.impeccable/review';mkdirSync(folder,{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const errors:string[]=[];
for(const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]] as const){
  const page=await browser.newPage({viewport:{width,height}});
  page.on('pageerror',error=>{errors.push(error.message);console.error('Wallet UI test page error: '+error.message);});
  // Controlled UI regression only: no real extension, account permission or transaction.
  await page.route('**/api/feed',route=>route.fulfill({json:{notes:Object.values(deployment.states).filter((state:unknown)=>state&&typeof state==='object'&&'history' in state),posts:{},addresses:deployment.contracts,hosts:deployment.states.config.hosts,unproven:deployment.unproven}}));
  // A literal browser script avoids tsx's Node-only function-name helpers.
  await page.addInitScript(`
    const state={mode:'pending-error',accounts:[],requests:[],approve:undefined};
    Object.assign(window,{footnoteWalletTest:state,ethereum:{request:async({method})=>{
      state.requests.push(method);
      if(method==='eth_accounts')return state.accounts;
      if(method==='eth_requestAccounts'){
        if(state.mode==='pending-error')throw {code:-32002,message:"Request of type 'wallet_requestPermissions' already pending for origin"};
        if(state.mode==='cancel')throw {code:4001,message:'User rejected the request.'};
        return new Promise(resolve=>{state.approve=()=>{state.accounts=['0x1111111111111111111111111111111111111111'];resolve(state.accounts);};});
      }
      if(method==='eth_chainId')return '0xf22f';
      if(method==='wallet_getSnaps')return {genlayer:{id:'npm:genlayer-wallet-plugin'}};
      throw Error('Unexpected method; no signing or transaction is permitted: '+method);
    }}});
  `);
  await page.goto(url,{waitUntil:'networkidle'});
  await page.getByRole('button',{name:'Connect wallet',exact:true}).click();
  await expect(page.locator('.error[role=alert]')).toContainText('Open your wallet extension and approve or cancel');
  await expect(page.getByRole('button',{name:'Connect wallet',exact:true})).toBeEnabled();
  await page.screenshot({path:folder+'/wallet-pending-error-'+name+'.png',fullPage:true});
  await page.evaluate(()=>Object.assign(Reflect.get(window,'footnoteWalletTest'),{mode:'cancel'}));
  await page.getByRole('button',{name:'Connect wallet',exact:true}).click();
  await expect(page.locator('.error[role=alert]')).toContainText('Wallet request cancelled');
  await page.evaluate(()=>Object.assign(Reflect.get(window,'footnoteWalletTest'),{mode:'wait',requests:[]}));
  await page.evaluate(()=>{for(let i=0;i<10;i++)(document.querySelector('.wallet') as HTMLButtonElement).click();});
  const waiting=page.getByRole('button',{name:'Waiting for wallet approval',exact:true});
  await expect(waiting).toBeDisabled();await expect(waiting).toHaveAttribute('aria-busy','true');
  await page.waitForFunction(()=>Reflect.get(window,'footnoteWalletTest').requests.includes('eth_requestAccounts'));
  expect(await page.evaluate(()=>Reflect.get(window,'footnoteWalletTest').requests.filter((method:string)=>method==='eth_requestAccounts').length)).toBe(1);
  await page.getByRole('button',{name:'Write a note',exact:true}).first().click();
  await expect(page.getByRole('button',{name:'Check your wallet…',exact:true})).toBeDisabled();
  await page.getByRole('button',{name:'Back to notes',exact:true}).click();
  await page.screenshot({path:folder+'/wallet-waiting-'+name+'.png',fullPage:true});
  await page.evaluate(()=>Reflect.get(window,'footnoteWalletTest').approve());
  await expect(page.getByRole('button',{name:'Connected wallet 0x1111111111111111111111111111111111111111',exact:true})).toBeEnabled();
  expect(await page.evaluate(()=>Reflect.get(window,'footnoteWalletTest').requests.filter((method:string)=>method==='eth_requestAccounts').length)).toBe(1);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)).toBe(false);
  await page.close();
}
await browser.close();
writeFileSync('docs/proofs/wallet-ui-check.json',JSON.stringify({checkedAt:new Date().toISOString(),url,viewports:[1440,390],errors,scope:'Mocked injected wallet and feed; no real permission, key, signature or transaction.',cases:['existing pending permission gives recovery instructions','cancellation recovers','ten gestures share one permission request','connect and write disabled while pending','approval completes connection']},null,2)+'\n');
if(errors.length)throw Error(errors.join('; '));
console.log('Desktop/mobile wallet checks passed: pending request, cancellation, concurrency, disabled controls and successful mocked approval. No live writes.');
