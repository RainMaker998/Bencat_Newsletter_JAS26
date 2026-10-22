// ===== v6 shaving effects =====
var RZ='<svg viewBox="0 0 36 36"><g transform="rotate(-40 18 18)"><rect x="5" y="4" width="26" height="9" rx="2.5" fill="currentColor" stroke="#fff" stroke-width="1.5"/><rect x="7" y="5.5" width="22" height="2" rx="1" fill="#CFE8FF"/><rect x="7" y="10" width="22" height="1.4" fill="#7FD3FF"/><rect x="16" y="13" width="4" height="20" rx="2" fill="#E06A10" stroke="#fff" stroke-width="1.2"/></g></svg>';
var HAIR_COLORS=['#2B1D14','#3B2A1E','#1A120C','#4A3626','#5C4632'];

// Hair clippings fall with gravity, drift and spin
function dropHair(x,y,n){
  n=n||14;
  for(var i=0;i<n;i++){
    var h=document.createElement('div');h.className='hair';
    var len=6+Math.random()*12,curl=(Math.random()-.5)*10,c=HAIR_COLORS[i%HAIR_COLORS.length];
    h.innerHTML='<svg width="'+(len+4)+'" height="14"><path d="M2 7 Q '+(len/2)+' '+(7+curl)+' '+(len+2)+' 7" stroke="'+c+'" stroke-width="'+(1+Math.random()*.9)+'" fill="none" stroke-linecap="round"/></svg>';
    h.style.left=(x-6+Math.random()*24)+'px';h.style.top=(y-4+Math.random()*6)+'px';
    document.body.appendChild(h);
    (function(el){
      var vx=(Math.random()-.5)*2.6,vy=-1.2-Math.random()*1.8,r=Math.random()*360,vr=(Math.random()-.5)*14,
          dx=0,dy=0,t=0,sway=Math.random()*6.28;
      function step(){
        t++;vy+=0.16;vx*=0.985;dx+=vx+Math.sin(t/9+sway)*0.5;dy+=Math.min(vy,4.2);r+=vr;
        el.style.transform='translate('+dx+'px,'+dy+'px) rotate('+r+'deg)';
        el.style.opacity=Math.max(0,1-t/85);
        if(t<85)requestAnimationFrame(step);else el.remove();
      }
      requestAnimationFrame(step);
    })(h);
  }
}
// A puff of shaving foam
function foam(x,y){
  for(var i=0;i<5;i++){var f=document.createElement('div');f.className='foam';var s=6+Math.random()*10;
    f.style.width=f.style.height=s+'px';f.style.left=(x-10+Math.random()*20)+'px';f.style.top=(y-10+Math.random()*14)+'px';
    f.style.animationDelay=(i*40)+'ms';document.body.appendChild(f);setTimeout(function(el){return function(){el.remove()}}(f),900);}
}
// A razor sweeps across an element (used when a panel or photo opens)
function sweep(rect){
  var s=document.createElement('div');s.className='sweep';s.innerHTML=RZ;document.body.appendChild(s);
  var y=rect.top+Math.min(rect.height,120)/2-32,x0=rect.left-40,x1=rect.right-20,t=0,N=28;
  (function step(){
    t++;var p=t/N,x=x0+(x1-x0)*(1-Math.pow(1-p,2));
    s.style.left=x+'px';s.style.top=(y+Math.sin(p*6.28)*6)+'px';s.style.transform='rotate('+(10-p*20)+'deg)';
    if(t%3===0)dropHair(x+30,y+48,3);
    if(t<N)requestAnimationFrame(step);else{s.style.transition='opacity .25s';s.style.opacity=0;setTimeout(function(){s.remove()},260);}
  })();
}

// Every click: hair falls where the razor touches
document.addEventListener('click',function(e){dropHair(e.clientX,e.clientY,12);foam(e.clientX,e.clientY);});

// Shave buttons: toggle panel whose id = data-target. Landed/Moving/Watch tiles act as one group.
document.querySelectorAll('.slice-btn').forEach(function(b){
  b.addEventListener('click',function(){
    var id=b.getAttribute('data-target'),p=document.getElementById(id),grp=b.classList.contains('tile');
    if(grp){document.querySelectorAll('.tile').forEach(function(t){var q=document.getElementById(t.getAttribute('data-target'));if(t!==b){t.classList.remove('open');q.classList.remove('open');}});}
    var o=p.classList.toggle('open');b.classList.toggle('open',o);
    if(o){
      var st=document.createElement('div');st.className='stroke';p.classList.add('shaving');p.appendChild(st);setTimeout(function(){st.remove()},750);
      setTimeout(function(){sweep(p.getBoundingClientRect());},120);
      if(!grp)setTimeout(function(){p.scrollIntoView({behavior:'smooth',block:'nearest'})},300);
    }
  });
});

// Lightbox with gallery navigation (Prev / Next, arrow keys, swipe)
var lb=document.getElementById('lb'),li=lb.querySelector('img'),list=[],idx=0;
var prev=document.createElement('button');prev.className='lb-nav lb-prev';prev.innerHTML='&#10094;';
var next=document.createElement('button');next.className='lb-nav lb-next';next.innerHTML='&#10095;';
var cnt=document.createElement('div');cnt.className='lb-count';
lb.appendChild(prev);lb.appendChild(next);lb.appendChild(cnt);

function show(i){
  idx=(i+list.length)%list.length;
  li.src=list[idx].src;li.classList.remove('shaved');void li.offsetWidth;li.classList.add('shaved');
  var multi=list.length>1;
  prev.style.display=next.style.display=cnt.style.display=multi?'':'none';
  cnt.textContent=(idx+1)+' / '+list.length;
  setTimeout(function(){sweep(li.getBoundingClientRect());},40);
}
// Open: photos inside a .gal group become a slideshow; single photos open alone
document.querySelectorAll('img.zoom').forEach(function(i){i.addEventListener('click',function(ev){
  ev.stopPropagation();dropHair(ev.clientX,ev.clientY,14);foam(ev.clientX,ev.clientY);
  var g=i.closest('.gal');list=g?Array.prototype.slice.call(g.querySelectorAll('img.zoom')):[i];
  lb.classList.add('show');show(list.indexOf(i));
});});
prev.addEventListener('click',function(e){e.stopPropagation();dropHair(e.clientX,e.clientY,8);show(idx-1);});
next.addEventListener('click',function(e){e.stopPropagation();dropHair(e.clientX,e.clientY,8);show(idx+1);});
// Click the photo itself = next (only in a gallery); click the dark background = close
li.addEventListener('click',function(e){if(list.length>1){e.stopPropagation();show(idx+1);}});
lb.addEventListener('click',function(){lb.classList.remove('show');});
// Keyboard: arrows to move, Esc to close
document.addEventListener('keydown',function(e){
  if(!lb.classList.contains('show'))return;
  if(e.key==='Escape')lb.classList.remove('show');
  if(e.key==='ArrowRight')show(idx+1);
  if(e.key==='ArrowLeft')show(idx-1);
});
// Touch: swipe left/right on phones & tablets
var tx=null;
lb.addEventListener('touchstart',function(e){tx=e.touches[0].clientX;},{passive:true});
lb.addEventListener('touchend',function(e){
  if(tx===null||list.length<2)return;var dx=e.changedTouches[0].clientX-tx;
  if(Math.abs(dx)>40)show(dx<0?idx+1:idx-1);tx=null;
});
