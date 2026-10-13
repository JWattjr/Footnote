import {chromium} from '@playwright/test';
import {mkdirSync,writeFileSync} from 'node:fs';
const folder='.impeccable/review';mkdirSync(folder,{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const errors:string[]=[];
for(const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]] as const){
  const page=await browser.newPage({viewport:{width,height}});page.on('pageerror',e=>errors.push(e.message));
  await page.goto(process.env.FOOTNOTE_URL??'http://localhost:3117',{waitUntil:'networkidle'});
  await page.getByRole('heading',{name:'Follow the evidence.'}).waitFor();
  await page.waitForFunction(()=>!document.body.innerText.includes('Opening the evidence desk'),{timeout:30000});
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  if(overflow)errors.push(name+' horizontal overflow');
  await page.screenshot({path:folder+'/'+name+'.png',fullPage:true});
  if(process.env.FOOTNOTE_LIVE_CHANGE_ID){
    const id=process.env.FOOTNOTE_LIVE_CHANGE_ID;
    await page.goto((process.env.FOOTNOTE_URL??'http://localhost:3117')+'/?note='+encodeURIComponent(id),{waitUntil:'networkidle'});
    await page.locator('.case-top').filter({hasText:id}).waitFor();
    if(await page.locator('.evidence-label strong').innerText()!=='Supported')errors.push(name+' live version 2 label missing');
    if(await page.locator('.history-list button').count()!==2)errors.push(name+' both live versions missing');
    const newSource='https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/';
    if(await page.locator('.source-section a').filter({has:page.locator('svg')}).evaluateAll((links,url)=>links.some(link=>(link as HTMLAnchorElement).href===url),newSource)!==true)errors.push(name+' new source missing');
    if(!await page.locator('.source-section blockquote').count())errors.push(name+' new source quote missing');
    if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))errors.push(name+' version 2 horizontal overflow');
    await page.screenshot({path:folder+'/label-change-'+name+'-v2.png',fullPage:true});
    await page.locator('.history-list button').filter({has:page.getByText('v1',{exact:true})}).click();
    await page.evaluate(()=>window.scrollTo(0,0));
    if(await page.locator('.evidence-label strong').innerText()!=='Unsupported')errors.push(name+' original Unsupported label missing');
    if(await page.locator('.source-section a').evaluateAll(links=>links.some(link=>(link as HTMLAnchorElement).href==='https://svs.gsfc.nasa.gov/4964/'))!==true)errors.push(name+' original source missing');
    if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))errors.push(name+' version 1 horizontal overflow');
    await page.screenshot({path:folder+'/label-change-'+name+'-v1.png',fullPage:true});
  }
  await page.getByRole('button',{name:'Write a note',exact:true}).first().click();
  await page.getByLabel('Note ID',{exact:true}).fill('browser-test');
  await page.getByLabel('Bluesky post AT URI').fill('invalid');
  await page.getByLabel('Source URLs').fill('https://evil.test/source');
  await page.getByRole('button',{name:'Stake bond',exact:true}).click();
  if(!await page.locator('.error[role=alert]').innerText().then(t=>t.includes('AT URI')))errors.push('Invalid URI not rejected');
  await page.getByRole('button',{name:'Back to notes',exact:true}).click();
  await page.getByRole('button',{name:'Live proof'}).click();
  if(await page.locator('.contract-list a').count()!==4)errors.push('Four explorer links missing');
  await page.goto((process.env.FOOTNOTE_URL??'http://localhost:3117')+'/replay',{waitUntil:'networkidle'});
  await page.getByRole('button',{name:'Apply mocked correction'}).click();
  if(await page.locator('.evidence-label strong').innerText()!=='Contradicted')errors.push('Test-only replay did not change label');
  await page.close();
}
await browser.close();writeFileSync(folder+'/browser-report.json',JSON.stringify({checkedAt:new Date().toISOString(),errors,viewports:[1440,390],url:process.env.FOOTNOTE_URL??'http://localhost:3117',liveLabelChangeNote:process.env.FOOTNOTE_LIVE_CHANGE_ID??null},null,2));
if(errors.length)throw Error(errors.join('; '));console.log('Desktop/mobile: render, form guards, explorer links, and no overflow passed.');
