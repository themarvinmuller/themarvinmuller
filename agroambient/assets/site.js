/* AgroAmbient: interações e efeitos de natureza. Cada bloco só roda se a página tiver o elemento. */
(function(){
  "use strict";
  var d=document, root=d.documentElement;
  root.classList.add("js");
  var reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var dpr=Math.min(2,window.devicePixelRatio||1);
  function $(id){return d.getElementById(id);}
  function rnd(seed){return function(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646;};}
  function smooth(t){t=Math.max(0,Math.min(1,t));return t*t*(3-2*t);}

  /* ---------- Título do herói palavra a palavra ---------- */
  var h1=$("heroTitle"), wi=0;
  if(h1){
    (function split(node){
      Array.prototype.slice.call(node.childNodes).forEach(function(n){
        if(n.nodeType===3){
          var frag=d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function(part){
            if(!part) return;
            if(/^\s+$/.test(part)){frag.appendChild(d.createTextNode(part));return;}
            var w=d.createElement("span");w.className="w";
            var s=d.createElement("span");s.textContent=part;s.style.setProperty("--i",wi++);
            w.appendChild(s);frag.appendChild(w);
          });
          node.replaceChild(frag,n);
        } else if(n.nodeType===1){ split(n); }
      });
    })(h1);
  }

  /* ---------- Fotos: placeholder quando não carregam ---------- */
  d.querySelectorAll(".photo img").forEach(function(img){
    function miss(){img.closest(".photo").classList.add("missing");}
    if(img.complete && img.naturalWidth===0 && img.getAttribute("src")) miss();
    img.addEventListener("error",miss);
  });

  /* ---------- Cabeçalho e menu ---------- */
  var head=d.querySelector(".site-head"), nav=$("nav"), mb=$("menuBtn"), mi=$("menuIcon");
  function setMenu(open){
    nav.classList.toggle("open",open); d.body.classList.toggle("menu-open",open);
    mb.setAttribute("aria-expanded",open); mb.setAttribute("aria-label",open?"Fechar menu":"Abrir menu");
    mi.setAttribute("d",open?"M6 6l16 16M22 6L6 22":"M4 9h20M4 19h20");
  }
  if(mb){
    mb.addEventListener("click",function(){setMenu(!nav.classList.contains("open"));});
    nav.addEventListener("click",function(e){if(e.target.closest("a")) setMenu(false);});
    d.addEventListener("keydown",function(e){if(e.key==="Escape"&&nav.classList.contains("open")){setMenu(false);mb.focus();}});
  }

  /* ---------- Revelação ---------- */
  var reveals=d.querySelectorAll(".reveal");
  if("IntersectionObserver" in window && !reduce){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});},{rootMargin:"0px 0px -8% 0px",threshold:.05});
    reveals.forEach(function(el){io.observe(el);});
  } else reveals.forEach(function(el){el.classList.add("in");});

  /* ---------- Siglas ---------- */
  var chips=$("chips"), out=$("chipOut");
  if(chips && window.AGRO_GLOSS){
    var gloss=window.AGRO_GLOSS;
    var show=function(k){
      var g=gloss[k];
      chips.querySelectorAll(".chip").forEach(function(c,j){c.setAttribute("aria-pressed",j===k);});
      out.innerHTML="";
      var s=d.createElement("strong");s.textContent=g[0]+" · "+g[1];
      var p=d.createElement("p");p.textContent=g[2];
      out.appendChild(s);out.appendChild(p);
      if(g[3]){var a=d.createElement("a");a.href=g[3];a.textContent="Saiba mais";a.className="more";out.appendChild(a);}
    };
    gloss.forEach(function(g,k){
      var b=d.createElement("button");b.type="button";b.className="chip";b.textContent=g[0];
      b.addEventListener("click",function(){show(k);});chips.appendChild(b);
    });
    show(0);
  }

  /* ---------- Copiar ---------- */
  d.querySelectorAll(".copy").forEach(function(b){
    b.addEventListener("click",function(){
      var el=$(b.dataset.copy), txt=el.textContent;
      function ok(){b.textContent="copiado";setTimeout(function(){b.textContent="copiar";},1600);}
      function fallback(){var r=d.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent="selecionado";}
      try{navigator.clipboard.writeText(txt).then(ok,fallback);}catch(e){fallback();}
    });
  });

  /* ---------- Formulário ---------- */
  var form=$("form");
  if(form){
    var params=new URLSearchParams(location.search), pre=params.get("assunto");
    var sel=$("f-assunto");
    if(pre){Array.prototype.forEach.call(sel.options,function(o){if(o.value===pre||o.text===pre) sel.value=o.value;});}
    var msg=$("formMsg");
    form.addEventListener("submit",function(e){
      e.preventDefault();
      var nome=$("f-nome");
      if(!nome.value.trim()){msg.textContent="Preencha seu nome para continuar.";nome.focus();return;}
      var cidade=$("f-cidade").value.trim(), texto=$("f-msg").value.trim();
      var lines=["Olá, AgroAmbient! Vim pelo site.","","*Nome:* "+nome.value.trim(),"*Assunto:* "+sel.value];
      if(cidade) lines.push("*Cidade:* "+cidade);
      if(texto) lines.push("","*Mensagem:* "+texto);
      var body=lines.join("\n"), wa=form.dataset.wa;
      window.agroTrack && window.agroTrack.lead(sel.value);
      if(wa){
        var url="https://wa.me/"+wa+"?text="+encodeURIComponent(body);
        var w=window.open(url,"_blank","noopener");
        if(!w) location.href=url;
        msg.textContent="Abrimos o WhatsApp com a sua mensagem. É só tocar em enviar.";
      }else{
        // Sem número de WhatsApp configurado (content.py → whatsapp_e164): cai no e-mail.
        var to=form.dataset.email||"agroambient@gmail.com";
        location.href="mailto:"+to+"?subject="+encodeURIComponent("Pedido pelo site: "+sel.value)+"&body="+encodeURIComponent(body.replace(/\*/g,""));
        msg.textContent="Abrimos seu aplicativo de e-mail com a mensagem pronta. Se ele não abrir, escreva para "+to+".";
      }
    });
  }
  var y=$("year"); if(y) y.textContent=new Date().getFullYear();

  /* ---------- FAQ: abre um por vez com animação suave ---------- */
  d.querySelectorAll(".faq details").forEach(function(det){
    det.addEventListener("toggle",function(){ if(det.open && window.agroTrack) window.agroTrack.event("faq_open",{pergunta:det.querySelector("summary").textContent.trim().slice(0,90)}); });
  });

  /* =========================================================
     HERÓI: Cerrado ao entardecer, camadas geradas + parallax
     ========================================================= */
  var scene=$("scene"), heroVisible=false, drawHero=null, applyParallax=null, sizeHero=null;
  var scrollY=0;
  if(scene){
    heroVisible=true;
    var NS="http://www.w3.org/2000/svg", W=1600, H=900;
    var ridge=function(base,amp,seed,mesas){
      var r=rnd(seed), ph=[r()*6,r()*6,r()*6], pts=[];
      for(var x=-20;x<=W+20;x+=8){
        var yv=base - amp*(0.5*Math.sin(x/260+ph[0]) + 0.3*Math.sin(x/120+ph[1]) + 0.2*Math.sin(x/53+ph[2]));
        (mesas||[]).forEach(function(m){var up=smooth((x-m[0])/m[3]), down=1-smooth((x-m[1])/m[3]);yv-=m[2]*Math.min(up,down);});
        pts.push([x,yv]);
      }
      var dd="M-20 "+H+" ";
      pts.forEach(function(p){dd+="L"+p[0].toFixed(1)+" "+p[1].toFixed(1)+" ";});
      return {d:dd+"L"+(W+20)+" "+H+"Z", pts:pts};
    };
    var yAt=function(pts,x){for(var k=1;k<pts.length;k++){if(pts[k][0]>=x){var a=pts[k-1],b=pts[k],t=(x-a[0])/(b[0]-a[0]);return a[1]+(b[1]-a[1])*t;}}return pts[pts.length-1][1];};
    var el=function(tag,attrs,parent){var e=d.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e;};
    var layer=function(depth){var svg=el("svg",{viewBox:"0 0 "+W+" "+H,preserveAspectRatio:"xMidYMax slice"});svg.dataset.depth=depth;scene.appendChild(svg);return svg;};
    var buriti=function(g,x,y,h,color,r){
      var lean=(r()-.5)*14;
      el("path",{d:"M"+x+" "+y+" Q"+(x+lean*.4)+" "+(y-h*.5)+" "+(x+lean)+" "+(y-h),stroke:color,"stroke-width":Math.max(2,h/38),fill:"none","stroke-linecap":"round"},g);
      var cx=x+lean, cy=y-h, n=13;
      for(var k=0;k<n;k++){
        var a=-Math.PI*0.94 + (Math.PI*0.88)*(k/(n-1)) + (r()-.5)*.12;
        var len=h*(.26+r()*.08), side=Math.cos(a);
        var mx=cx+side*len*.6, my=cy+Math.sin(a)*len*.75;
        var ex=cx+side*len*1.05, ey=cy+Math.sin(a)*len*.45 + Math.abs(side)*len*.38;
        el("path",{d:"M"+cx+" "+cy+" Q"+mx+" "+my+" "+ex+" "+ey,stroke:color,"stroke-width":Math.max(1.4,h/70),fill:"none","stroke-linecap":"round"},g);
      }
      el("path",{d:"M"+cx+" "+cy+" l-2 -"+(h*.16)+" M"+cx+" "+cy+" l3 -"+(h*.14),stroke:color,"stroke-width":Math.max(1.4,h/60),fill:"none"},g);
      el("ellipse",{cx:cx,cy:cy+h*.03,rx:h*.028,ry:h*.045,fill:color},g);
    };
    var cerradoTree=function(g,x,y,h,color,r){
      el("path",{d:"M"+x+" "+y+" q"+(r()*10-5)+" -"+(h*.4)+" "+(r()*16-8)+" -"+(h*.6)+" M"+x+" "+(y-h*.45)+" q12 -8 "+(18+r()*10)+" -"+(h*.25),stroke:color,"stroke-width":h/16,fill:"none","stroke-linecap":"round"},g);
      for(var k=0;k<5;k++) el("ellipse",{cx:x+(r()-.5)*h*.8,cy:y-h*(.62+r()*.25),rx:h*(.2+r()*.14),ry:h*(.1+r()*.06),fill:color},g);
    };
    var seed0=+(scene.dataset.seed||1);
    var layers=[];
    var sunL=layer(0.08);
    var defs=el("defs",{},sunL), grad=el("radialGradient",{id:"sunGlow"},defs);
    [["0","#FFF2C2","1"],[".18","#FFD979",".95"],[".45","#F7A75A",".25"],["1","#F7A75A","0"]].forEach(function(s){el("stop",{offset:s[0],"stop-color":s[1],"stop-opacity":s[2]},grad);});
    var sunX=900+((seed0*137)%500);
    el("circle",{cx:sunX,cy:560,r:340,fill:"url(#sunGlow)"},sunL);
    var sunDisc=el("circle",{cx:sunX,cy:560,r:62,fill:"#FFE7A3"},sunL);
    layers.push(sunL);
    var specs=[
      {base:640,amp:30,seed:7, color:"#9B6A79", mesas:[[120,620,95,60],[1300,1700,70,50]], depth:.16},
      {base:690,amp:38,seed:21,color:"#6E4C62", mesas:[[700,1050,60,45]], depth:.28, trees:{n:10,h:[40,60],kind:"tree"}},
      {base:745,amp:26,seed:44,color:"#3D3346", depth:.42, trees:{n:9,h:[110,170],kind:"buriti"}},
      {base:815,amp:20,seed:90,color:"#1C1D25", depth:.62, trees:{n:5,h:[200,280],kind:"buriti"}, grass:true}
    ];
    specs.forEach(function(s){
      var sd=s.seed*seed0, L=layer(s.depth), r=rnd(sd*13), rg=ridge(s.base,s.amp,sd,s.mesas), g=el("g",{},L);
      el("path",{d:rg.d,fill:s.color},g);
      if(s.trees){
        for(var k=0;k<s.trees.n;k++){
          var x=60+r()*(W-120), h=s.trees.h[0]+r()*(s.trees.h[1]-s.trees.h[0]), yy=yAt(rg.pts,x)+4;
          if(s.trees.kind==="buriti") buriti(g,x,yy,h,s.color,r); else cerradoTree(g,x,yy,h,s.color,r);
        }
      }
      if(s.grass){
        var gd="";
        for(var gx=-10;gx<W+10;gx+=5+r()*6){
          var gy=yAt(rg.pts,gx)+6, hh=14+r()*34, bend=(r()-.3)*18;
          gd+="M"+gx.toFixed(1)+" "+gy.toFixed(1)+" q"+(bend*.3).toFixed(1)+" -"+(hh*.6).toFixed(1)+" "+bend.toFixed(1)+" -"+hh.toFixed(1)+" ";
        }
        el("path",{d:gd,stroke:s.color,"stroke-width":2.2,fill:"none","stroke-linecap":"round"},L);
      }
      layers.push(L);
    });
    var mist=d.createElement("div");
    mist.style.cssText="position:absolute;left:0;right:0;bottom:16%;height:22%;background:linear-gradient(180deg,transparent,rgba(242,180,140,.18),transparent);pointer-events:none";
    scene.insertBefore(mist,layers[3]);
    var veil=d.createElement("div"); veil.className="veil"; scene.appendChild(veil);
    var cv=d.createElement("canvas"); scene.appendChild(cv);
    var ctx=cv.getContext("2d"), cw=0, ch=0;
    sizeHero=function(){cw=scene.clientWidth;ch=scene.clientHeight;cv.width=cw*dpr;cv.height=ch*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);};
    sizeHero();
    var R=rnd(99), flies=[], birds=[];
    for(var f=0;f<46;f++) flies.push({x:R(),y:.55+R()*.45,vx:(R()-.5)*.0004,vy:(R()-.5)*.0003,p:R()*6.28,s:1+R()*2});
    var flock=function(){
      var n=5+Math.floor(R()*4), yb=.12+R()*.22, sp=.00045+R()*.0003;
      for(var b=0;b<n;b++) birds.push({x:1.1+b*.025+R()*.02,y:yb+(b%2?1:-1)*b*.012+R()*.01,sp:sp,p:R()*6.28,s:5+R()*3});
    };
    flock();
    var mx=0,my=0,tx=0,ty=0;
    window.addEventListener("pointermove",function(e){tx=(e.clientX/window.innerWidth-.5);ty=(e.clientY/window.innerHeight-.5);},{passive:true});
    drawHero=function(t){
      ctx.clearRect(0,0,cw,ch);
      flies.forEach(function(q){
        q.x+=q.vx+Math.sin(t/1800+q.p)*.0002; q.y+=q.vy+Math.cos(t/2100+q.p)*.00015;
        if(q.x<0)q.x=1;if(q.x>1)q.x=0;if(q.y<.45)q.y=1;if(q.y>1)q.y=.5;
        var a=Math.max(0,Math.sin(t/700+q.p*3)); a=a*a;
        var x=q.x*cw, yq=q.y*ch, r=q.s*5;
        var g=ctx.createRadialGradient(x,yq,0,x,yq,r);
        g.addColorStop(0,"rgba(255,236,150,"+(.9*a)+")");g.addColorStop(1,"rgba(255,200,80,0)");
        ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,yq,r,0,6.283);ctx.fill();
      });
      ctx.strokeStyle="rgba(28,24,40,.75)";ctx.lineWidth=1.6;ctx.lineCap="round";
      for(var k=birds.length-1;k>=0;k--){
        var b=birds[k]; b.x-=b.sp; var flap=Math.sin(t/140+b.p)*.55;
        var x=b.x*cw, yb=b.y*ch+Math.sin(t/900+b.p)*4, s=b.s;
        ctx.beginPath();ctx.moveTo(x-s,yb-s*flap);ctx.quadraticCurveTo(x-s*.4,yb-s*.15,x,yb);ctx.quadraticCurveTo(x+s*.4,yb-s*.15,x+s,yb-s*flap);ctx.stroke();
        if(b.x<-.1) birds.splice(k,1);
      }
      if(!birds.length && R()<.004) flock();
    };
    applyParallax=function(){
      mx+=(tx-mx)*.05; my+=(ty-my)*.05;
      var sy=Math.min(scrollY,ch);
      for(var k=0;k<layers.length;k++){
        var dep=+layers[k].dataset.depth;
        layers[k].style.transform="translate3d("+(-mx*60*dep)+"px,"+(sy*(0.5-dep*.6)+(-my*18*dep))+"px,0)";
      }
      sunDisc.setAttribute("cy",560+sy*.25);
    };
    new IntersectionObserver(function(es){heroVisible=es[0].isIntersecting;}).observe(scene.parentElement);
  }

  /* =========================================================
     RIO: peixes que fogem do cursor, raios de luz e bolhas
     ========================================================= */
  var rc=$("riverCanvas"), riverVisible=false, drawRiver=null, rsize=null;
  if(rc){
    var rx=rc.getContext("2d"), rw=0, rh=0;
    rsize=function(){rw=rc.clientWidth;rh=rc.clientHeight;rc.width=rw*dpr;rc.height=rh*dpr;rx.setTransform(dpr,0,0,dpr,0,0);};
    rsize();
    var RR=rnd(5), fish=[], bubbles=[], pointer={x:-999,y:-999};
    for(var q=0;q<26;q++){var dir=RR()<.5?-1:1; fish.push({x:RR()*1.2-.1,y:.18+RR()*.75,dir:dir,sp:.0006+RR()*.0009,s:10+RR()*22,p:RR()*6.28,dx:0,dy:0,depth:.4+RR()*.6});}
    for(var q2=0;q2<40;q2++) bubbles.push({x:RR(),y:RR(),r:1+RR()*3,sp:.0006+RR()*.0012,p:RR()*6});
    rc.parentElement.addEventListener("pointermove",function(e){var b=rc.getBoundingClientRect();pointer.x=e.clientX-b.left;pointer.y=e.clientY-b.top;},{passive:true});
    rc.parentElement.addEventListener("pointerleave",function(){pointer.x=pointer.y=-999;});
    drawRiver=function(t){
      var g=rx.createLinearGradient(0,0,0,rh);
      g.addColorStop(0,"#1A7480");g.addColorStop(.35,"#0E4F59");g.addColorStop(1,"#062B31");
      rx.fillStyle=g;rx.fillRect(0,0,rw,rh);
      rx.save();rx.globalCompositeOperation="lighter";
      for(var k=0;k<6;k++){
        var x=rw*(k/6)+Math.sin(t/3000+k)*60, w=60+k%3*40;
        var lg=rx.createLinearGradient(0,0,0,rh*.9);lg.addColorStop(0,"rgba(190,240,230,.12)");lg.addColorStop(1,"rgba(190,240,230,0)");
        rx.fillStyle=lg;rx.beginPath();rx.moveTo(x,0);rx.lineTo(x+w,0);rx.lineTo(x+w*2.4+160,rh*.9);rx.lineTo(x+160,rh*.9);rx.closePath();rx.fill();
      }
      rx.restore();
      rx.strokeStyle="rgba(220,250,245,.35)";rx.lineWidth=2;rx.beginPath();
      for(var x2=0;x2<=rw;x2+=12){var yy=10+Math.sin(x2/60+t/600)*4+Math.sin(x2/23+t/350)*2;if(x2===0)rx.moveTo(x2,yy);else rx.lineTo(x2,yy);}
      rx.stroke();
      rx.fillStyle="rgba(220,250,245,.35)";
      bubbles.forEach(function(b){b.y-=b.sp;if(b.y<0){b.y=1;b.x=RR();}rx.beginPath();rx.arc(b.x*rw+Math.sin(t/500+b.p)*6,b.y*rh,b.r,0,6.283);rx.fill();});
      fish.forEach(function(f){
        f.x+=f.sp*f.dir;
        if(f.x>1.15)f.x=-.15;if(f.x<-.15)f.x=1.15;
        var px=f.x*rw+f.dx, py=f.y*rh+Math.sin(t/700+f.p)*6+f.dy;
        var ddx=px-pointer.x, ddy=py-pointer.y, dist=Math.sqrt(ddx*ddx+ddy*ddy);
        if(dist<150&&dist>0){var force=(150-dist)/150*4;f.dx+=ddx/dist*force;f.dy+=ddy/dist*force;}
        f.dx*=.95;f.dy*=.95;
        var s=f.s, wig=Math.sin(t/120+f.p)*.35;
        rx.save();rx.translate(px,py);rx.scale(f.dir,1);
        rx.fillStyle="rgba(200,236,226,"+(.18+f.depth*.32)+")";
        rx.beginPath();rx.ellipse(0,0,s,s*.36,0,0,6.283);rx.fill();
        rx.beginPath();rx.moveTo(-s*.85,0);rx.lineTo(-s*1.45,-s*.4+wig*s*.3);rx.lineTo(-s*1.45,s*.4+wig*s*.3);rx.closePath();rx.fill();
        rx.beginPath();rx.moveTo(-s*.1,-s*.3);rx.lineTo(s*.25,-s*.62);rx.lineTo(s*.35,-s*.28);rx.closePath();rx.fill();
        rx.restore();
      });
    };
    new IntersectionObserver(function(es){riverVisible=es[0].isIntersecting;}).observe(rc.parentElement);
  }

  /* ---------- Folhas caindo ---------- */
  var lc=$("leaves"), leavesVisible=false, drawLeaves=null, lsize=null;
  if(lc){
    var lx=lc.getContext("2d"), lw=0, lh=0, LR=rnd(17), leaves=[];
    lsize=function(){lw=lc.clientWidth;lh=lc.clientHeight;lc.width=lw*dpr;lc.height=lh*dpr;lx.setTransform(dpr,0,0,dpr,0,0);};
    lsize();
    var leafCols=["rgba(217,154,18,.55)","rgba(141,203,162,.35)","rgba(196,110,60,.4)"];
    for(var l=0;l<22;l++) leaves.push({x:LR(),y:LR(),s:6+LR()*10,sp:.0004+LR()*.0006,p:LR()*6.28,rot:LR()*6.28,c:leafCols[l%3]});
    drawLeaves=function(t){
      lx.clearRect(0,0,lw,lh);
      leaves.forEach(function(f){
        f.y+=f.sp; if(f.y>1.05){f.y=-.05;f.x=LR();}
        var x=f.x*lw+Math.sin(t/1400+f.p)*40, yy=f.y*lh, r=f.rot+Math.sin(t/900+f.p)*1.2;
        lx.save();lx.translate(x,yy);lx.rotate(r);lx.fillStyle=f.c;
        lx.beginPath();lx.moveTo(0,-f.s);lx.quadraticCurveTo(f.s*.7,0,0,f.s);lx.quadraticCurveTo(-f.s*.7,0,0,-f.s);lx.fill();
        lx.restore();
      });
    };
    new IntersectionObserver(function(es){leavesVisible=es[0].isIntersecting;}).observe(lc.parentElement);
  }

  /* ---------- Painel horizontal da fauna ---------- */
  var fauna=$("fauna"), track=$("faunaTrack"), bar=$("faunaBar"), horizontal=false;
  function setupFauna(){
    if(!fauna) return;
    horizontal=!reduce && window.innerWidth>760;
    if(!horizontal){fauna.style.height="";track.style.transform="";return;}
    var extra=track.scrollWidth-window.innerWidth;
    fauna.style.height=(window.innerHeight+Math.max(0,extra))+"px";
  }
  function updateFauna(){
    if(!fauna||!horizontal) return;
    var r=fauna.getBoundingClientRect(), total=fauna.offsetHeight-window.innerHeight;
    var p=Math.max(0,Math.min(1,-r.top/Math.max(1,total)));
    var extra=Math.max(0,track.scrollWidth-window.innerWidth);
    track.style.transform="translate3d("+(-p*extra)+"px,0,0)";
    bar.style.transform="scaleX("+p+")";
  }

  /* ---------- Trilha do processo ---------- */
  var pw=$("processWrap"), tfg=$("trailFg"), tbg=$("trailBg"), trail=$("trail"), steps=d.querySelectorAll(".step"), tlen=0;
  function setupTrail(){
    if(!pw) return;
    var h=pw.offsetHeight; trail.setAttribute("viewBox","0 0 40 "+h); trail.style.height=h+"px";
    var dd="M2 28", seg=60;
    for(var yv=28;yv<h-40;yv+=seg){ var dir=((yv/seg)|0)%2?1:-1; dd+=" q"+(dir*14)+" "+(seg/2)+" 0 "+seg; }
    tbg.setAttribute("d",dd);tfg.setAttribute("d",dd);
    tlen=tfg.getTotalLength(); tfg.style.strokeDasharray=tlen; tfg.style.strokeDashoffset=tlen;
  }
  function updateTrail(){
    if(!pw) return;
    var r=pw.getBoundingClientRect(), vh=window.innerHeight;
    var p=Math.max(0,Math.min(1,(vh*.6-r.top)/r.height));
    tfg.style.strokeDashoffset=tlen*(1-p);
    steps.forEach(function(s){var b=s.getBoundingClientRect();s.classList.toggle("lit",b.top<vh*.6);});
  }

  /* ---------- Barra de leitura (artigos) ---------- */
  var rbar=$("readBar"), article=d.querySelector("article.prose");
  function updateRead(){
    if(!rbar||!article) return;
    var r=article.getBoundingClientRect(), total=r.height-window.innerHeight*.5;
    rbar.style.transform="scaleX("+Math.max(0,Math.min(1,-r.top/Math.max(1,total)))+")";
  }

  /* ---------- Loop ---------- */
  var solidAt=scene?0.6:0.05;
  function onScroll(){
    scrollY=window.scrollY||window.pageYOffset;
    if(head) head.classList.toggle("solid",scrollY>Math.max(40,(scene?scene.clientHeight:window.innerHeight)*solidAt));
    updateFauna(); updateTrail(); updateRead();
  }
  window.addEventListener("scroll",onScroll,{passive:true});
  window.addEventListener("resize",function(){sizeHero&&sizeHero();rsize&&rsize();lsize&&lsize();setupFauna();setupTrail();onScroll();});
  setupFauna(); setupTrail(); onScroll();
  drawHero&&drawHero(0); drawRiver&&drawRiver(0); drawLeaves&&drawLeaves(0); applyParallax&&applyParallax();
  if(!reduce){
    (function frame(t){
      if(heroVisible&&drawHero){drawHero(t);applyParallax();}
      if(riverVisible&&drawRiver) drawRiver(t);
      if(leavesVisible&&drawLeaves) drawLeaves(t);
      requestAnimationFrame(frame);
    })(0);
  }
})();
