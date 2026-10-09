document.documentElement.classList.remove("no-js");
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');
const parcelSprite = new Image();
parcelSprite.src = 'assets/parcel-material.webp';
parcelSprite.addEventListener('load', () => draw());
const roads = [...document.querySelectorAll('svg path')].map(path => ({path, length:path.getTotalLength()}));
let playing = !reduced.matches, heroVisible = true, t = 0, last = 0, raf = 0;
function resizeHero(){
 const scale=Math.min(2,devicePixelRatio||1)*canvas.getBoundingClientRect().width/1672;
 canvas.width=Math.round(1672*scale);canvas.height=Math.round(941*scale);
 ctx.setTransform(canvas.width/1672,0,0,canvas.height/941,0,0);draw();
}
function draw() {
 ctx.clearRect(0,0,1672,941);
 const parcels=roads.flatMap((road,i)=>{
  const local=(t+18+6-i*4)%18;
  if(!reduced.matches&&local>16)return [];
  const progress=reduced.matches?[.65,.78,.58][i]:Math.min(1,local/12);
  const point=road.path.getPointAtLength(progress*road.length);
  return [{x:point.x,y:point.y,size:42+(point.y-440)*.06,alpha:reduced.matches?1:Math.min(1,local*2,(16-local)*2)}];
 }).sort((a,b)=>a.y-b.y);
 for(const {x,y,size,alpha} of parcels){
  ctx.save();ctx.globalAlpha=alpha;ctx.translate(x,y);
  if(parcelSprite.complete && parcelSprite.naturalWidth) {
   ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';
   ctx.drawImage(parcelSprite,-size*.625,-size*1.14,size*1.25,size*1.25);
  }
  ctx.restore();
 }
}
new ResizeObserver(resizeHero).observe(canvas);
window.addEventListener('resize',resizeHero);
function loop(now) {
 if (!playing || reduced.matches || !heroVisible || document.hidden) {raf=0;last=0;return;}
 if (last) t+=Math.min(.05,(now-last)/1000);
 last=now; draw(); raf=requestAnimationFrame(loop);
}
function syncHero() {

 if (!playing || reduced.matches || !heroVisible || document.hidden) {cancelAnimationFrame(raf);raf=0;last=0;}
 else if (!raf) raf=requestAnimationFrame(loop);
}
draw();syncHero();


const grid=document.querySelector('.channel-grid');
const buttons=[...document.querySelectorAll('[data-filter]')];
const rows=[...grid.children];
// Keep each route visually recognizable when editorial ordering changes.
rows.forEach((row,index)=>{row.dataset.tone=String(index%5);row.dataset.shape=(index%7===1||index%11===2)?'tall':index%9===4?'short':'regular';});
const editorialOrder={"companion": ["智玩店", "凯知乐", "上海亿嘟", "广东瑞华行", "AI机器时代", "永华嘉业", "上海贝杰", "迅合行"], "learning": ["璞康", "七色花", "武汉京天电器", "华森葳", "新烨数码", "智玩店", "上海亿嘟", "山东振强具身智能"], "wearable": ["智玩店", "博士／总统眼镜", "三夫户外", "爱施德", "上海锐能体育", "九机", "北京广世天运"], "home": ["沐诺智家", "DK-AI", "好享家", "E宠", "音联邦", "京东五星电器", "中智关爱通"], "office": ["科力普", "伟仕佳杰", "欧菲斯", "英迈中国", "史泰博", "华为云云商店", "美承"], "creative": ["传新科技", "INNO100", "雅登乐器", "美承", "翰林汇", "柏斯音乐", "中智关爱通"]};
const originalIndex=new Map(rows.map((row,index)=>[row,index]));
function orderForDirection(direction){const priority=editorialOrder[direction]||[];const rank=row=>{const i=priority.indexOf(row.querySelector(".channel-name").textContent);return i<0?priority.length+originalIndex.get(row):i;};[...rows].sort((a,b)=>rank(a)-rank(b)).forEach(row=>grid.append(row));}
const search=document.querySelector('.channel-search');
const query=document.querySelector('#channel-query');
let flowing=!reduced.matches, flowVisible=false, flowLast=0, flowStart=0, flowRaf=0, position=0;
function syncFlow() {

 const eligible=!document.querySelector('.network-stage').classList.contains('is-expanded') && flowing && !reduced.matches && flowVisible && !document.hidden && grid.scrollHeight>grid.clientHeight+2;
 if (!eligible) {cancelAnimationFrame(flowRaf);flowRaf=0;flowLast=0;flowStart=0;}
 else if (!flowRaf) {position=grid.scrollTop;flowRaf=requestAnimationFrame(tick);}
}
function tick(now) {
 if (!flowing || reduced.matches || !flowVisible || document.hidden) {flowRaf=0;flowLast=0;return;}
 if (!flowStart) flowStart=now;
 if (now-flowStart>1200 && flowLast) {
  position+=Math.min(.05,(now-flowLast)/1000)*18;
  const end=grid.scrollHeight-grid.clientHeight;
  grid.scrollTop=Math.min(position,end);
  if (position>=end) {flowing=false;syncFlow();return;}
 }
 flowLast=now; flowRaf=requestAnimationFrame(tick);
}
function pauseFlow(){flowing=false;syncFlow();}

for (const type of ['pointerenter','pointerdown','focusin','keydown','touchstart'])grid.addEventListener(type,pauseFlow,{passive:true});
grid.addEventListener('wheel',pauseFlow,{passive:true});
// Only broaden well-defined business words already present in the display tags.
const queryAliases={音频:['音频','音响','录音'],礼赠:['礼赠','礼品','福礼','福利'],企业采购:['企业采购','企业集采']};
function matchesQuery(row,term){
 const text=(row.textContent+' '+(row.dataset.search||'')).normalize('NFKC').toLocaleLowerCase();
 return term.split(/\s+/).filter(Boolean).every(token=>(queryAliases[token]||[token]).some(word=>text.includes(word)));
}
function filter(button, {alignToResults=false}={}) {
 document.querySelector('#network').dataset.direction=button.dataset.filter;
 pauseFlow();
 // Preserve spatial continuity when a product direction narrows the field.
 rows.forEach(row=>row.getAnimations().forEach(animation=>animation.cancel()));
 const before=new Map(rows.filter(row=>!row.hidden).map(row=>[row,row.getBoundingClientRect()]));buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 orderForDirection(button.dataset.filter);
 const term=query.value.trim().normalize('NFKC').toLocaleLowerCase();
 rows.forEach(row=>{const direction=button.dataset.filter==='all'||row.dataset.directions.split(' ').includes(button.dataset.filter);const matches=matchesQuery(row,term);row.hidden=!(direction&&matches);});
 document.querySelector('.search-empty').hidden=rows.some(row=>!row.hidden);
 grid.scrollTop=0;
 if (alignToResults && document.querySelector('.network-stage').classList.contains('is-expanded')) {
  const controls=document.querySelector('.network-toolbar');
  window.scrollTo({top:grid.getBoundingClientRect().top+window.scrollY-controls.offsetHeight-32,behavior:'instant'});
 }
 document.querySelector('.browse-status').textContent=!rows.some(row=>!row.hidden)?'暂未找到相关通路。':term?`已显示与${query.value.trim()}相关的通路。`:button.dataset.filter==='all'?'已显示全部市场通路。':`已显示${button.textContent}相关通路。`;
 if (!reduced.matches) {
  rows.filter(row=>!row.hidden).forEach((row,index)=>{
   const previous=before.get(row), next=row.getBoundingClientRect();
   const old=previous && Math.abs(previous.top-next.top)<grid.clientHeight ? previous : null;
   const frames=old
    ? [{transform:`translate(${old.left-next.left}px,${old.top-next.top}px)`,opacity:1},{transform:'translate(0,0)',opacity:1}]
    : [{transform:'translateY(14px)',opacity:0},{transform:'translateY(0)',opacity:1}];
   row.animate(frames,{duration:old?420:320,delay:old?0:Math.min(index,8)*22,easing:'cubic-bezier(.22,1,.36,1)'});
  });
 }
}
search.onsubmit=event=>event.preventDefault();
let searchTimer;
query.addEventListener('input',event=>{if(event.isComposing)return;clearTimeout(searchTimer);searchTimer=setTimeout(()=>filter(buttons.find(b=>b.getAttribute('aria-pressed')==='true')),120);});
query.addEventListener('compositionend',()=>{clearTimeout(searchTimer);filter(buttons.find(b=>b.getAttribute('aria-pressed')==='true'));});
search.addEventListener('reset',()=>{clearTimeout(searchTimer);query.value='';filter(buttons.find(b=>b.getAttribute('aria-pressed')==='true'));query.focus();});
buttons.forEach((button,index)=>{
 button.onclick=()=>filter(button,{alignToResults:true});
 button.onkeydown=event=>{
  let next;
  if(event.key==='ArrowRight')next=(index+1)%buttons.length;
  else if(event.key==='ArrowLeft')next=(index+buttons.length-1)%buttons.length;
  else if(event.key==='Home')next=0;
  else if(event.key==='End')next=buttons.length-1;
  else return;
  event.preventDefault();buttons[next].focus();filter(buttons[next]);
 };
});
if ('IntersectionObserver' in window) {
 new IntersectionObserver(entries=>{heroVisible=entries[0].isIntersecting;syncHero();},{threshold:.01}).observe(document.querySelector('.landscape'));
 new IntersectionObserver(entries=>{flowVisible=entries[0].isIntersecting;syncFlow();},{threshold:.3}).observe(grid);
}
document.addEventListener('visibilitychange',()=>{syncHero();syncFlow();});
reduced.addEventListener('change',()=>{playing=!reduced.matches;if(reduced.matches)flowing=false;draw();syncHero();syncFlow();});
filter(buttons[0]);
syncHero();syncFlow();

const expand=document.querySelector('.expand-network');
const collapse=document.querySelector('.collapse-network');
let expansionAnimation;
function setExpanded(expanded) {
 expansionAnimation?.cancel();
 const previousHeight=grid.getBoundingClientRect().height;
 pauseFlow();
 expand.setAttribute('aria-expanded',String(expanded));
 document.querySelector('.network-stage').classList.toggle('is-expanded',expanded);
 document.querySelector('#network').classList.toggle('is-expanded',expanded);
 expand.textContent=expanded?'收起通路 ↑':'查看更多通路 ↗';
 collapse.hidden=!expanded;
 if(expanded&&!reduced.matches){
  const targetHeight=grid.getBoundingClientRect().height;
  expansionAnimation=grid.animate([{height:previousHeight+'px',overflow:'hidden'},{height:targetHeight+'px',overflow:'hidden'}],{duration:Math.min(780,350+(targetHeight-previousHeight)*.06),easing:'cubic-bezier(.22,1,.36,1)'});
 }
 if (!expanded) {
  grid.scrollTop=0;
  document.querySelector('.network-toolbar').scrollIntoView({block:'start',behavior:reduced.matches?'instant':'smooth'});
  buttons.find(button=>button.getAttribute('aria-pressed')==='true')?.focus({preventScroll:true});
 }
}
expand.onclick=()=>setExpanded(expand.getAttribute('aria-expanded')!=='true');
collapse.onclick=()=>setExpanded(false);

// The cue follows real overflow, including filtering, resizing and full expansion.
(()=>{const stage=document.querySelector('.network-stage');const list=stage.querySelector('.channel-grid');const update=()=>{const bounded=!stage.classList.contains('is-expanded');stage.classList.toggle('has-content-above',bounded&&list.scrollTop>2);stage.classList.toggle('has-content-below',bounded&&list.scrollTop+list.clientHeight<list.scrollHeight-2);};list.addEventListener('scroll',update,{passive:true});new ResizeObserver(update).observe(list);new MutationObserver(update).observe(stage,{attributes:true,attributeFilter:['class']});new MutationObserver(update).observe(list,{subtree:true,attributes:true,attributeFilter:['hidden']});update();})();
