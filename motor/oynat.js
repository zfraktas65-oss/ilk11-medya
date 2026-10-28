
const D = window.__DATA; let anims=null, cur=-2;
const scenes=[...document.querySelectorAll('.scene')];
// karakterli çizgi film sahneleri (motor/cizgi.js): her karede sahne içi zamana göre yeniden çizilir
const CZ=[...document.querySelectorAll('.cizgi')].map(el=>({el,p:JSON.parse(el.getAttribute('data-p')),i:scenes.indexOf(el.closest('.scene'))}));
const subs=document.getElementById('subs'); const lb=document.getElementById('label'); const rz=document.getElementById('rozet');
function ease(x){x=Math.max(0,Math.min(1,x));return 1-Math.pow(1-x,3)}
function init(){scenes.forEach(s=>s.style.visibility='visible');
 anims=document.getAnimations(); anims.forEach(a=>{a.pause(); const el=a.effect&&a.effect.target;
 const sc=el&&el.closest?el.closest('.scene'):null; a._st=sc?parseFloat(sc.dataset.start):0;});}
function seek(t){ if(!anims) init();
 anims.forEach(a=>{a.currentTime=Math.max(0,t-a._st)*1000;});
 CZ.forEach(c=>{const s=D.scenes[c.i]; if(s&&t>=s.start-0.05&&t<s.end+0.35) c.el.innerHTML=CIZGI.draw(c.p,t-s.start,s.end-s.start,c.i);});
 D.scenes.forEach((s,i)=>{const el=scenes[i]; let o=0;
  if(t>=s.start && t<s.end+0.3){o = i==0?1:ease((t-s.start)/0.28);}
  el.style.visibility=o>0.001?'visible':'hidden'; el.style.opacity=o;});
 lb.style.opacity = t < D.labelEnd ? 1 : Math.max(0, 1-(t-D.labelEnd)/0.3);
 if(rz && D.rozetA!=null){const a=D.rozetA; const k=(t>=a&&t<D.labelEnd)?Math.min(ease((t-a)/0.35),ease((D.labelEnd-t)/0.3)):0;
  rz.style.opacity=k; rz.style.transform=`translateX(-50%) scale(${0.8+0.2*k})`;
  if(t>=a) lb.style.opacity=Math.min(parseFloat(lb.style.opacity), Math.max(0,1-(t-a)/0.25));}
 let k=-1; D.chunks.forEach((c,j)=>{if(t>=c.t0&&t<c.end)k=j;});
 if(k!==cur){cur=k; subs.innerHTML=k<0?'':D.chunks[k].w.map(w=>`<span>${w[0]}</span>`).join(' ');}
 if(k>=0){const c=D.chunks[k], sp=subs.children, a=ease((t-c.t0)/0.15);
  subs.style.opacity=a; subs.style.transform=`scale(${0.92+0.08*a})`;
  c.w.forEach((w,j)=>{sp[j].className=(t>=w[1]-0.03&&t<w[2]+0.08)?'on':(t<w[1]?'next':'');});}
 else subs.style.opacity=0;
 return true;}
document.fonts.ready.then(()=>{init();seek(0);window.__ready=true;});
