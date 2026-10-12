import {readFileSync} from 'node:fs';
import {readClient,read} from '../lib/network';
const p=JSON.parse(readFileSync('public/deployment.json','utf8'));
const wallet=p.states['climate-record'].writer as `0x${string}`;
const bonds=p.contracts.bonds as `0x${string}`;
const client=readClient();
const [walletBalance,bondsBalance,totals]=await Promise.all([client.getBalance({address:wallet}),client.getBalance({address:bonds}),read(bonds,'get_totals')]);
console.log(JSON.stringify({wallet,walletBalance:String(walletBalance),bondsBalance:String(bondsBalance),totals:JSON.parse(String(totals))},null,2));
