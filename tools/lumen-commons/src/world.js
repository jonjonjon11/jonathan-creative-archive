/* Original cached-vector 2.5D renderer. No imported artwork, game engine or network. */
(function () {
'use strict';
const C = window.LumenCore, TAU = Math.PI*2;
const SKINS = ['#f4d2b4','#dfb18d','#c98f66','#ac704d','#84523e','#593a32'];
function ellipse(c,x,y,rx,ry,color){c.fillStyle=color;c.beginPath();c.ellipse(x,y,rx,ry,0,0,TAU);c.fill();}
function poly(c,points,color,stroke){c.beginPath();points.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p));c.closePath();c.fillStyle=color;c.fill();if(stroke){c.strokeStyle=stroke;c.lineWidth=1.5;c.stroke();}}
function line(c,points,color,width=2){c.beginPath();points.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p));c.strokeStyle=color;c.lineWidth=width;c.lineCap='round';c.lineJoin='round';c.stroke();}
function box(c,x,y,w,h,r,color){c.fillStyle=color;c.beginPath();c.roundRect(x,y,w,h,r);c.fill();}
const glowCache=new Map();
function glow(c,x,y,r,color){const key=r+color;if(!glowCache.has(key)){const a=document.createElement('canvas');a.width=a.height=r*2;const q=a.getContext('2d'),g=q.createRadialGradient(r,r,1,r,r,r);g.addColorStop(0,color);g.addColorStop(1,'transparent');ellipse(q,r,r,r,r,g);glowCache.set(key,a);}c.drawImage(glowCache.get(key),x-r,y-r);}
function sprite(w,h,draw){const a=document.createElement('canvas');a.width=w;a.height=h;draw(a.getContext('2d'));return a;}
function rng(seed){return()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};}
const STATIONS = [
 {id:'fractions',x:490,y:500,color:'#f8d18a',symbol:'⅗',kind:'forge',npc:'Tavi'},
 {id:'trajectory',x:1100,y:510,color:'#88e8d4',symbol:'↗',kind:'lab',npc:'Mira'},
 {id:'harmony',x:565,y:765,color:'#e9ace9',symbol:'♫',kind:'music',npc:'Sora'},
 {id:'orbit',x:830,y:290,color:'#b8baff',symbol:'◉',kind:'observatory',npc:'Ari'},
 {id:'coordinates',x:1200,y:755,color:'#addd92',symbol:'⌖',kind:'garden',npc:'Noor'},
 {id:'cafe',x:330,y:710,color:'#f2c6a0',symbol:'♧',kind:'cafe',npc:'Jun'}
];
class World {
 constructor(canvas,map,state,onEnter,onMote,onHint){
  this.canvas=canvas;this.c=canvas.getContext('2d',{alpha:false});this.map=map;this.mc=map.getContext('2d');this.state=state;this.onEnter=onEnter;this.onMote=onMote;this.onHint=onHint;
  this.p={x:800,y:700};this.cam={x:800,y:555};this.target=null;this.keys=new Set();this.joy={x:0,y:0};this.t=0;this.pulse=0;this.cooldown=0;this.paused=false;this.moving=false;this.facing=1;this.fps=0;this.acc=0;this.n=0;this.mapClock=0;
  this.r=rng(12);this.sprites={};this.makeSprites();this.makeTerrain();this.makeDecor();
  this.motes=Array.from({length:12},(_,i)=>({id:i,x:800+Math.cos(i*TAU/12)*390,y:565+Math.sin(i*TAU/12)*240}));
  this.stars=Array.from({length:55},()=>({x:this.r(),y:this.r(),r:this.r()*1.4+.3}));
  this.resize=()=>{const rect=canvas.getBoundingClientRect();this.w=rect.width;this.h=rect.height;this.dpr=Math.min(window.devicePixelRatio||1,{low:1,balanced:1.5,high:2}[state.quality]);canvas.width=Math.round(this.w*this.dpr);canvas.height=Math.round(this.h*this.dpr);this.zoom=this.w<580?.86:Math.min(.9,Math.max(.65,Math.min(this.w/1450,this.h/1050)));};
  this.ro=new ResizeObserver(this.resize);this.ro.observe(canvas);this.resize();this.bind();this.last=0;
  this.frame=this.frame.bind(this);requestAnimationFrame(this.frame);
 }
 makeSprites(){
  this.sprites.tree=sprite(150,185,c=>{
   ellipse(c,76,163,47,16,'#163d383b');poly(c,[[70,158],[84,158],[85,85],[73,75]],'#745e45');line(c,[[78,130],[49,107]],'#746447',8);line(c,[[80,120],[111,95]],'#746447',6);
   const leaves=[[75,77,49,51,'#285c51'],[41,87,34,30,'#326d59'],[102,85,35,38,'#3c8061'],[71,49,38,33,'#579575'],[50,54,29,27,'#6ba581'],[90,43,30,27,'#79b68b'],[105,64,26,27,'#669b71']];
   leaves.forEach(v=>ellipse(c,...v));line(c,[[55,38],[72,34],[83,36]],'#aad0a080',3);ellipse(c,110,55,4,4,'#c4dda1');
  });
  this.sprites.pinktree=sprite(150,180,c=>{
   ellipse(c,76,159,42,14,'#15333033');line(c,[[78,155],[80,80]],'#8c7569',12);line(c,[[78,124],[49,91]],'#8c7569',7);line(c,[[79,116],[106,77]],'#8c7569',6);
   [[80,62,48,41,'#ac8eb0'],[43,80,30,28,'#c6a3bd'],[108,79,29,31,'#b7a1b9'],[63,39,33,27,'#e4c4cb'],[94,41,30,31,'#d7bac8'],[43,59,28,25,'#ead0cd']].forEach(v=>ellipse(c,...v));
  });
  this.sprites.rock=sprite(90,75,c=>{ellipse(c,45,62,39,10,'#173a3a40');poly(c,[[8,53],[19,22],[50,10],[75,27],[85,57],[51,64]],'#6b8e86');poly(c,[[19,22],[50,10],[75,27],[46,42]],'#a7b7a0');poly(c,[[46,42],[75,27],[85,57],[51,64]],'#52766b');});
  this.sprites.lamp=sprite(80,165,c=>{ellipse(c,40,151,17,6,'#14332944');line(c,[[40,148],[40,45]],'#51665a',5);line(c,[[39,47],[57,47],[57,56]],'#6b8170',3);glow(c,55,65,35,'#ffeb9f65');box(c,47,56,18,21,5,'#d7b477');box(c,50,59,12,14,4,'#fff0b2');ellipse(c,40,146,7,3,'#a6ac87');});
  this.sprites.crystal=sprite(100,180,c=>{
   ellipse(c,50,155,44,15,'#385f59');ellipse(c,50,147,40,14,'#b0c7a6');ellipse(c,50,146,31,10,'#5f9690');glow(c,50,81,48,'#8af8c960');poly(c,[[50,25],[76,84],[50,125],[25,84]],'#b5eed1','#e8ffe2');poly(c,[[50,25],[50,125],[25,84]],'#6bbfc3');poly(c,[[50,25],[76,84],[51,79]],'#dbffde');line(c,[[27,84],[51,79],[73,84]],'#f3ffe880',2);
  });
  for(const s of STATIONS)this.sprites[s.kind]=this.building(s.kind);
 }
 building(kind){return sprite(270,250,c=>{
  ellipse(c,133,221,115,25,'#163a4145');
  if(kind==='observatory'){
   ellipse(c,133,211,102,30,'#5e7b78');ellipse(c,133,199,102,30,'#bfceba');box(c,70,121,124,77,7,'#abc0b1');poly(c,[[70,122],[131,139],[131,218],[70,199]],'#658d8b');poly(c,[[131,139],[194,122],[194,199],[131,218]],'#819c8c');
   const g=c.createLinearGradient(60,20,180,140);g.addColorStop(0,'#b8c7df');g.addColorStop(.5,'#6d92b1');g.addColorStop(1,'#405975');c.fillStyle=g;c.beginPath();c.ellipse(132,121,74,82,0,Math.PI,0);c.closePath();c.fill();ellipse(c,132,121,74,21,'#789fba');line(c,[[132,40],[145,119]],'#e3d7ac',5);poly(c,[[139,72],[191,33],[204,48],[154,91]],'#cecdb3','#698895');ellipse(c,197,41,12,11,'#88b8b5');ellipse(c,197,41,7,7,'#1d435b');box(c,149,156,23,35,10,'#344e5a');box(c,151,159,19,17,6,'#c1e9d6');ellipse(c,108,65,11,18,'#e0eff02a');
  }else if(kind==='cafe'){
   poly(c,[[36,128],[126,151],[228,123],[228,204],[126,237],[36,207]],'#c8ba91');poly(c,[[36,128],[126,151],[126,237],[36,207]],'#b59c72');poly(c,[[126,151],[228,123],[228,204],[126,237]],'#dfcda2');poly(c,[[21,131],[126,47],[244,117],[128,163]],'#466d60');poly(c,[[21,131],[126,47],[128,163]],'#679583');line(c,[[21,131],[128,163],[244,117]],'#9db798',7);line(c,[[126,51],[128,162]],'#b8c9a0',3);
   box(c,151,165,32,48,4,'#597368');box(c,155,170,24,25,3,'#e7daa0');poly(c,[[46,155],[91,168],[91,196],[46,182]],'#506e61');poly(c,[[52,160],[85,170],[85,187],[52,176]],'#ffe4a0');poly(c,[[134,153],[225,128],[235,149],[139,177]],'#c87767');line(c,[[145,151],[155,171]],'#efd0aa',6);line(c,[[170,143],[180,163]],'#efd0aa',6);line(c,[[198,136],[208,154]],'#efd0aa',6);glow(c,217,184,25,'#ffe7a749');box(c,211,171,11,21,3,'#ffe3a0');line(c,[[216,162],[216,172]],'#67593e',2);ellipse(c,65,215,26,9,'#8b7953');line(c,[[65,216],[65,232]],'#665b45',5);ellipse(c,65,211,29,9,'#e0c89a');ellipse(c,59,210,5,3,'#f2eed5');ellipse(c,70,208,4,3,'#90b483');
  }else if(kind==='garden'){
   ellipse(c,138,203,99,27,'#9eaf8f');poly(c,[[51,123],[130,148],[221,120],[221,191],[130,222],[51,196]],'#537f7288');poly(c,[[44,122],[130,50],[229,114],[132,153]],'#7eceb480','#c5ecd1');poly(c,[[51,123],[130,148],[130,220],[51,196]],'#67ac9566','#b9d9bb');poly(c,[[130,148],[221,120],[221,191],[130,222]],'#91d3b577','#b9d9bb');line(c,[[130,53],[130,219]],'#d3dfb8',5);line(c,[[51,123],[51,196]],'#d3dfb8',4);line(c,[[220,122],[220,192]],'#d3dfb8',4);line(c,[[87,90],[176,131],[176,205]],'#c7dfb8',3);line(c,[[177,79],[91,138],[91,207]],'#c7dfb8',3);
   [[75,183],[109,195],[168,183],[198,176]].forEach(([x,y])=>{poly(c,[[x-13,y],[x+13,y],[x+9,y+20],[x-8,y+20]],'#b99168');line(c,[[x,y],[x,y-31]],'#325d46',3);ellipse(c,x-10,y-24,13,6,'#aac88e');ellipse(c,x+9,y-34,13,6,'#bddda4');});
  }else if(kind==='music'){
   ellipse(c,135,207,105,30,'#527b78');ellipse(c,135,200,105,28,'#b7c6ad');ellipse(c,135,196,92,23,'#829e87');[58,210].forEach(x=>{line(c,[[x,180],[x,90]],'#dfd9ac',6);ellipse(c,x,181,9,4,'#b6b88d');});poly(c,[[35,93],[132,40],[231,93],[135,120]],'#9a859e');poly(c,[[35,93],[132,40],[135,120]],'#c2a9b9');line(c,[[35,93],[135,120],[231,93]],'#edd8c0',5);
   line(c,[[97,175],[108,119],[164,128],[154,190]],'#e9cf93',9);line(c,[[108,119],[152,185]],'#f8e8b8',3);for(let i=0;i<5;i++)line(c,[[115+i*8,123+i*1.2],[112+i*8,177+i*2]],'#e8e4c3',1);glow(c,139,149,49,'#efc6eb25');ellipse(c,57,110,10,13,'#f7d6a3');ellipse(c,208,111,10,13,'#f7d6a3');
  }else{
   poly(c,[[60,132],[139,156],[222,130],[222,205],[138,229],[60,204]],kind==='forge'?'#b2ad85':'#8cae9e');poly(c,[[60,132],[139,156],[139,229],[60,204]],kind==='forge'?'#928b6c':'#648e88');poly(c,[[43,132],[133,67],[235,126],[137,163]],kind==='forge'?'#6c9280':'#59988e');poly(c,[[43,132],[133,67],[137,163]],kind==='forge'?'#96b298':'#8dc4ae');line(c,[[43,132],[137,163],[235,126]],'#cee0b0',5);box(c,163,164,28,44,5,'#3a685f');box(c,167,168,20,25,3,kind==='forge'?'#f9dd90':'#b3ead9');poly(c,[[73,158],[115,169],[115,196],[73,184]],'#425f51');poly(c,[[79,165],[109,172],[109,188],[79,180]],'#e2d49a');
   if(kind==='forge'){line(c,[[80,101],[80,52],[98,52],[98,90]],'#aea183',15);ellipse(c,89,48,15,7,'#6c7564');}else{line(c,[[136,92],[136,41]],'#d3d9b1',5);ellipse(c,136,36,16,16,'#a2e6d6');glow(c,136,36,30,'#96ffce50');line(c,[[118,57],[154,57]],'#e0ebc4',3);}
  }
 });}
 makeTerrain(){
  const r=rng(127);
  this.ground=sprite(1600,1120,c=>{
   ellipse(c,802,633,668,402,'#182d4670');ellipse(c,800,613,687,389,'#385159');
   for(let i=0;i<30;i++){const a=i*TAU/30,b=(i+1)*TAU/30,x=800+Math.cos(a)*680,y=563+Math.sin(a)*396,xx=800+Math.cos(b)*680,yy=563+Math.sin(b)*396;poly(c,[[x,y],[xx,yy],[810+(xx-800)*.84,yy+90+r()*80],[810+(x-800)*.82,y+95+r()*70]],['#45605e','#527468','#3d5b58','#638271'][i%4]);}
   const g=c.createLinearGradient(0,150,0,930);g.addColorStop(0,'#9bb997');g.addColorStop(.5,'#88ab8b');g.addColorStop(1,'#669886');ellipse(c,800,560,682,395,g);c.strokeStyle='#c5d5ab';c.lineWidth=5;c.beginPath();c.ellipse(800,560,682,395,0,0,TAU);c.stroke();
   ellipse(c,840,605,237,170,'#8fb699');ellipse(c,1016,699,123,72,'#446f78');ellipse(c,1016,693,116,65,'#63a4a3');ellipse(c,1010,689,100,54,'#77bcad');
   for(let i=0;i<18;i++){const x=920+r()*190,y=660+r()*70;line(c,[[x,y],[x+14+r()*20,y]],'#bae0c855',1.5);}
   // Soft roads; the paths remain decorative, not a false physical simulation.
   const roads=[[[780,585],[805,350]],[[765,585],[500,493]],[[840,585],[1108,503]],[[771,645],[555,752]],[[731,643],[358,699]],[[865,605],[1230,735]]];
   roads.forEach(p=>{line(c,p,'#708d7655',64);line(c,p,'#bfca9d',53);line(c,p,'#cdd1a9',37);});
   ellipse(c,800,610,117,71,'#99ae88');ellipse(c,800,603,111,66,'#d0d3ad');ellipse(c,800,603,92,54,'#7faba0');ellipse(c,800,603,78,44,'#bdd4b1');ellipse(c,800,603,69,38,'#83b9ab');
   for(let i=0;i<12;i++){const a=i*TAU/12;ellipse(c,800+Math.cos(a)*98,603+Math.sin(a)*59,3.5,2,'#faf0cb');}
   for(let i=0;i<380;i++){const x=135+r()*1340,y=190+r()*754;if(!C.inside(x,y)||Math.hypot((x-800)/2,y-610)<140)continue;const k=r();if(k<.6){line(c,[[x,y],[x-2,y-5],[x+1,y-2],[x+4,y-6]],'#4a8c6955',1);}else{ellipse(c,x,y,2+r()*2,1.5,['#e5d9a5','#c3dbaf','#c9b8ce'][i%3]);}}
   for(let i=0;i<36;i++){const a=i*TAU/36,x=800+Math.cos(a)*654,y=560+Math.sin(a)*371;ellipse(c,x,y,12+r()*14,4+r()*5,'#8bb58a');}
  });
 }
 makeDecor(){
  this.decor=[];const r=rng(92);
  for(let i=0;i<26;i++){const a=i*TAU/26,x=800+Math.cos(a)*(550+r()*55),y=550+Math.sin(a)*(298+r()*25);if(STATIONS.some(s=>Math.hypot(s.x-x,s.y-y)<160))continue;this.decor.push({x,y,kind:i%4===0?'pinktree':'tree',scale:.82+r()*.4});}
  [[625,385],[1010,370],[260,580],[1325,639],[723,835],[398,810]].forEach((p,i)=>this.decor.push({x:p[0],y:p[1],kind:i%2?'pinktree':'tree',scale:.85}));
  [[670,500],[973,501],[653,678],[871,795],[420,625],[1090,820]].forEach(p=>this.decor.push({x:p[0],y:p[1],kind:'lamp',scale:.75}));
  [[210,645],[982,840],[1283,441],[565,300],[1390,600],[356,842]].forEach(p=>this.decor.push({x:p[0],y:p[1],kind:'rock',scale:.6}));
 }
 blocked(x,y){return STATIONS.some(s=>Math.hypot((x-s.x)/1.1,y-(s.y-60))<60)||Math.hypot((x-1016)/1.75,y-693)<65||Math.hypot((x-800)/1.5,y-586)<37;}
 bind(){
  window.addEventListener('keydown',e=>{if(this.paused||/INPUT|SELECT|TEXTAREA|BUTTON/.test(e.target.tagName))return;if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' ','w','a','s','d','W','A','S','D','e','E'].includes(e.key)){e.preventDefault();this.keys.add(e.key.toLowerCase());this.target=null;if(e.key.toLowerCase()==='e')this.interact();if(e.key===' ')this.resonate();}});
  window.addEventListener('keyup',e=>this.keys.delete(e.key.toLowerCase()));
  window.addEventListener('blur',()=>{this.keys.clear();this.joy={x:0,y:0};});
  document.addEventListener('visibilitychange',()=>{this.keys.clear();this.joy={x:0,y:0};this.last=0;});
  this.canvas.addEventListener('pointerdown',e=>{if(this.paused)return;const rect=this.canvas.getBoundingClientRect(),x=(e.clientX-rect.left-this.w/2)/this.zoom+this.cam.x,y=(e.clientY-rect.top-this.h/2)/this.zoom+this.cam.y;const s=STATIONS.find(s=>Math.hypot(x-s.x,y-(s.y-32))<66);if(s){this.visit(s.id);return;}if(C.inside(x,y)&&!this.blocked(x,y)){this.target={x,y};this.canvas.focus({preventScroll:true});}});
 }
 visit(id){const s=STATIONS.find(s=>s.id===id);if(!s)return;this.p={x:s.x+35,y:s.y+42};this.target=null;this.keys.clear();this.onEnter(id);}
 nearest(){return STATIONS.reduce((a,b)=>Math.hypot(b.x-this.p.x,b.y-this.p.y)<Math.hypot(a.x-this.p.x,a.y-this.p.y)?b:a);}
 interact(){const s=this.nearest();if(Math.hypot(s.x-this.p.x,s.y-this.p.y)<135)this.onEnter(s.id);else this.onHint('nearby');}
 resonate(){if(this.cooldown>0||this.paused)return;this.pulse=.001;this.cooldown=1.2;for(const m of this.motes)if(!this.state.motes.includes(m.id)&&Math.hypot(m.x-this.p.x,m.y-this.p.y)<150)this.onMote(m.id);}
 setPaused(v){this.paused=v;this.keys.clear();this.joy={x:0,y:0};this.target=null;}
 drawSprite(kind,x,y,scale=1){const a=this.sprites[kind];if(a)this.c.drawImage(a,x-a.width*scale/2,y-a.height*scale+15,a.width*scale,a.height*scale);}
 character(x,y,skin,color,time,walking=false,face=1,player=false){const c=this.c,step=walking&&!this.state.reduced?Math.sin(time*12):0,bob=this.state.reduced?0:Math.sin(time*(walking?24:3))*1.5;
  c.save();c.translate(x,y);ellipse(c,0,3,19,7,'#12353642');c.translate(0,bob);c.scale(face,1);
  if(player){poly(c,[[-5,-29],[-24-step*2,-18],[-19,-34],[-2,-38]],'#eec17e');}
  line(c,[[-7,-18],[-7+step*3,-3]],'#3d555e',7);line(c,[[7,-18],[7-step*3,-3]],'#3d555e',7);ellipse(c,-7+step*3,-1,6,3,'#e8d9bc');ellipse(c,7-step*3,-1,6,3,'#e8d9bc');
  box(c,-12,-39,24,24,8,color);poly(c,[[0,-38],[9,-38],[10,-18],[0,-18]],'#ffffff16');line(c,[[-12,-34],[-16-step*2,-20]],SKINS[skin],6);line(c,[[12,-34],[15+step*2,-20]],SKINS[skin],6);
  ellipse(c,0,-49,13,15,SKINS[skin]);ellipse(c,-12,-48,3,4,SKINS[skin]);ellipse(c,12,-48,3,4,SKINS[skin]);ellipse(c,0,-59,14,10,skin<2?'#86654b':'#354446');poly(c,[[-13,-59],[-14,-47],[-7,-57],[5,-57],[10,-53],[13,-59]],skin<2?'#86654b':'#354446');ellipse(c,-4,-49,1.5,2,'#273c39');ellipse(c,6,-49,1.5,2,'#273c39');line(c,[[-1,-43],[3,-43]],'#744b3e',1);box(c,-11,-39,23,5,2,player?'#f2ce87':'#c0dbc0');
  if(player){ellipse(c,0,-27,3,3,'#e8f4b4');line(c,[[-10,-23],[10,-23]],'#8bd4bb',1);}
  c.restore();
 }
 render(){const c=this.c,w=this.w,h=this.h,t=this.state.reduced?0:this.t;c.setTransform(this.dpr,0,0,this.dpr,0,0);
  const sky=c.createLinearGradient(0,0,w*.5,h);sky.addColorStop(0,'#253946');sky.addColorStop(.5,'#526a70');sky.addColorStop(1,'#719684');c.fillStyle=sky;c.fillRect(0,0,w,h);
  const effects={low:12,balanced:30,high:55}[this.state.quality];
  for(let i=0;i<effects;i++){const s=this.stars[i];ellipse(c,s.x*w,(s.y*h*.8+t*2)%h,s.r,s.r,'#d8ead65a');}
  // Distant floating islands: parallax silhouettes, intentionally original.
  for(let i=0;i<4;i++){const x=(i*.36*w+160-this.cam.x*.07)%(w+230)-70,y=180+i%2*85-this.cam.y*.03;poly(c,[[x-90,y],[x,y-23],[x+120,y],[x+40,y+50],[x-19,y+80]],'#6a8f8855');ellipse(c,x+13,y,105,19,'#9eb9a04a');line(c,[[x+45,y+12],[x+45,y+115]],'#bde2d526',11);}
  c.save();c.translate(w/2,h/2);c.scale(this.zoom,this.zoom);c.translate(-this.cam.x,-this.cam.y);
  c.drawImage(this.ground,0,0);
  if(!this.state.reduced){for(let i=0;i<3;i++){line(c,[[455+i*10,885],[455+i*10,960+Math.sin(t+i)*14]],'#c4ecda77',6);}}
  // Glowing discoveries, all bounded and rendered without per-particle filters.
  for(const m of this.motes){if(this.state.motes.includes(m.id))continue;const yy=m.y+Math.sin(t*2+m.id)*4;glow(c,m.x,yy-8,18,'#e7f8ad4f');poly(c,[[m.x,yy-17],[m.x+5,yy-8],[m.x,yy],[m.x-5,yy-8]],'#edf2b6');ellipse(c,m.x,yy+6,7,2,'#dbeabd44');}
  if(this.target){c.strokeStyle='#eff5c5';c.lineWidth=2;c.beginPath();c.ellipse(this.target.x,this.target.y,13,6,0,0,TAU);c.stroke();}
  const objects=this.decor.map(d=>({y:d.y,draw:()=>this.drawSprite(d.kind,d.x,d.y,d.scale)}));
  objects.push({y:608,draw:()=>this.drawSprite('crystal',800,610,.9)});
  STATIONS.forEach((s,i)=>{
   objects.push({y:s.y-22,draw:()=>this.drawSprite(s.kind,s.x,s.y-15,.88)});
   objects.push({y:s.y+25,draw:()=>{this.character(s.x-47,s.y+25,(i+1)%6,['#b88872','#719aac','#a78faa','#708d81','#8a9e6c','#bc9075'][i],t+i,false,-1);}});
  });
  objects.push({y:this.p.y,draw:()=>this.character(this.p.x,this.p.y,this.state.skin,'#589d94',t,this.moving,this.facing,true)});
  objects.sort((a,b)=>a.y-b.y).forEach(o=>o.draw());
  STATIONS.forEach((s,i)=>{
   const done=this.state.complete.includes(s.id),yy=s.y-178,fade=.6+Math.sin(t*2+i)*.12;
   if(done)glow(c,s.x,s.y-99,88,s.color+'44');
   c.save();c.translate(s.x+47,s.y-55);c.scale(1,.7);c.strokeStyle=done?'#e5ffc9':s.color;c.lineWidth=3;c.beginPath();c.ellipse(0,0,21,36,0,0,TAU);c.stroke();c.globalAlpha=fade;ellipse(c,0,0,16,29,s.color+'2c');c.restore();
   const name=this.labels?this.labels[i]:s.id.toUpperCase();c.font='600 10px system-ui';const tw=c.measureText(name).width;box(c,s.x-tw/2-12,yy-15,tw+24,24,7,'#13322cce');c.fillStyle=done?'#e3f7bb':'#eef0d7';c.textAlign='center';c.fillText((done?'✓ ':'')+name,s.x,yy+1);c.font='8px system-ui';c.fillStyle='#eaf0d9';c.fillText(s.npc+' · NPC',s.x-47,s.y-42);
  });
  // A visibly non-human local guide follows the explorer.
  const bx=this.p.x+32,by=this.p.y-54+Math.sin(t*3)*5;glow(c,bx,by,24,'#e7f4b833');ellipse(c,bx,by,11,9,'#ecf1cb');ellipse(c,bx+2,by,7,5,'#759d90');ellipse(c,bx,by-1,1,1.7,'#263a37');ellipse(c,bx+4,by-1,1,1.7,'#263a37');line(c,[[bx-9,by],[bx-16,by-6-Math.sin(t*9)*3]],'#e4edc9',3);
  if(this.pulse>0&&!this.state.reduced){c.strokeStyle='#edffd0';c.lineWidth=3;c.globalAlpha=Math.max(0,1-this.pulse);c.beginPath();c.ellipse(this.p.x,this.p.y,20+this.pulse*130,10+this.pulse*65,0,0,TAU);c.stroke();c.globalAlpha=1;}
  if(effects>12){for(let i=0;i<effects/2;i++){const x=300+(i*91)%1050+Math.sin(t*.5+i)*17,y=280+(i*127)%520-Math.sin(t*.8+i)*10;ellipse(c,x,y,1.7,1.7,i%3?'#eaf0be99':'#f3c6db99');}}
  c.restore();
 }
 renderMap(){const c=this.mc;c.clearRect(0,0,168,104);ellipse(c,84,52,72,40,'#527969');c.strokeStyle='#b7cba2';c.lineWidth=1;c.beginPath();c.ellipse(84,52,72,40,0,0,TAU);c.stroke();STATIONS.forEach(s=>ellipse(c,84+(s.x-800)*.102,52+(s.y-560)*.1,3,3,this.state.complete.includes(s.id)?'#e9ffb8':s.color));ellipse(c,84+(this.p.x-800)*.102,52+(this.p.y-560)*.1,4,4,'#ffffff');}
 frame(ms){requestAnimationFrame(this.frame);if(document.hidden){this.last=0;return;}if(!this.last){this.last=ms;return;}const interval=this.paused?100:(this.state.quality==='low'?1000/30:1000/60);if(ms-this.last<interval-1)return;const raw=(ms-this.last)/1000,dt=Math.min(raw,.05);this.last=ms;this.t+=this.paused?0:dt;this.cooldown=Math.max(0,this.cooldown-dt);if(this.pulse>0){this.pulse+=dt*1.5;if(this.pulse>1)this.pulse=0;}
  this.acc+=raw;this.n++;if(this.acc>=1){this.fps=Math.round(this.n/this.acc);this.n=0;this.acc=0;}
  this.moving=false;
  if(!this.paused){let dx=(this.keys.has('d')||this.keys.has('arrowright')?1:0)-(this.keys.has('a')||this.keys.has('arrowleft')?1:0)+this.joy.x,dy=(this.keys.has('s')||this.keys.has('arrowdown')?1:0)-(this.keys.has('w')||this.keys.has('arrowup')?1:0)+this.joy.y;
   if(this.target&&!dx&&!dy){dx=this.target.x-this.p.x;dy=this.target.y-this.p.y;if(Math.hypot(dx,dy)<5){this.target=null;dx=dy=0;}}
   const old=this.p;this.p=C.move(this.p,dx,dy,dt,180,(x,y)=>this.blocked(x,y));this.moving=Math.hypot(this.p.x-old.x,this.p.y-old.y)>.01;if(dx)this.facing=dx>0?1:-1;if(this.target&&!this.moving)this.target=null;
   this.cam.x+=(C.clamp(this.p.x,520,1080)-this.cam.x)*Math.min(1,dt*4);this.cam.y+=(C.clamp(this.p.y-135,420,640)-this.cam.y)*Math.min(1,dt*4);
   for(const m of this.motes)if(!this.state.motes.includes(m.id)&&Math.hypot(m.x-this.p.x,m.y-this.p.y)<30)this.onMote(m.id);
  }
  this.render();this.mapClock+=dt;if(this.mapClock>.12){this.renderMap();this.mapClock=0;}
 }
}
window.LumenWorld=World;window.LumenStations=STATIONS;window.LumenSkins=SKINS;
})();
