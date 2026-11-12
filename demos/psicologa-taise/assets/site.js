/* Taise Ferreira: interações no mesmo modelo do site AgroAmbient, em versão clara. */
(function(){
  "use strict";
  var d=document, root=d.documentElement;
  root.classList.add("js");
  var reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var dpr=Math.min(2,window.devicePixelRatio||1);
  var WA="5562982226820";
  function $(id){return d.getElementById(id);}
  function rnd(seed){return function(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646;};}

  /* ---------- Links de WhatsApp ---------- */
  var waText="Olá, Taise! Vim pelo site e gostaria de marcar uma primeira conversa.";
  d.querySelectorAll("[data-wa]").forEach(function(a){
    a.href="https://wa.me/"+WA+"?text="+encodeURIComponent(waText); a.target="_blank"; a.rel="noopener";
  });

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

  /* ---------- Menu ---------- */
  var head=d.querySelector(".site-head"), nav=$("nav"), mb=$("menuBtn"), mi=$("menuIcon");
  function setMenu(open){
    nav.classList.toggle("open",open);
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

  /* ---------- Glossário da psicanálise ---------- */
  var GLOSS=[
    ["Associação livre","Falar o que vier, sem filtro","É a regra básica da análise: você fala o que passa pela cabeça, mesmo o que parece sem importância, confuso ou constrangedor. É por esse caminho que aparece o que não estava à vista."],
    ["Escuta","Atenção ao que é dito e ao como","A analista escuta com atenção o que você conta, as repetições, as pausas e as palavras que escapam. Não é uma conversa comum, nem um conselho."],
    ["Inconsciente","O que age em nós sem que a gente saiba","Parte do que sentimos e fazemos tem motivos que não conhecemos. Eles aparecem nos sonhos, nos esquecimentos, nos atos falhos e nos sintomas."],
    ["Sintoma","Um sofrimento que carrega um sentido","Na psicanálise, o sintoma não é só algo a eliminar. Ele diz alguma coisa sobre a sua história, e escutá-lo é parte do trabalho."],
    ["Transferência","O vínculo que se forma na análise","Com o tempo, a relação com a analista passa a repetir modos de se relacionar que você tem com outras pessoas. Isso vira material de trabalho."],
    ["Elaboração","Dar contorno ao que antes só doía","Falar várias vezes sobre algo, de jeitos diferentes, permite que aquilo ganhe sentido e pese de outra forma."]
  ];
  var chips=$("chips"), out=$("chipOut");
  if(chips){
    var show=function(k){
      var g=GLOSS[k];
      chips.querySelectorAll(".chip").forEach(function(c,j){c.setAttribute("aria-pressed",j===k);});
      out.innerHTML="";
      var s=d.createElement("strong");s.textContent=g[0]+" · "+g[1];
      var p=d.createElement("p");p.textContent=g[2];
      out.appendChild(s);out.appendChild(p);
    };
    GLOSS.forEach(function(g,k){
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

  /* ---------- Formulário: abre o WhatsApp com a mensagem pronta ---------- */
  var form=$("form");
  if(form){
    var msg=$("formMsg");
    form.addEventListener("submit",function(e){
      e.preventDefault();
      var nome=$("f-nome");
      if(!nome.value.trim()){msg.textContent="Escreva seu nome para continuar.";nome.focus();return;}
      var lines=["Olá, Taise! Vim pelo site.","","Nome: "+nome.value.trim(),"Atendimento: "+$("f-modo").value,"Melhor período: "+$("f-periodo").value];
      var texto=$("f-msg").value.trim();
      if(texto) lines.push("","Mensagem: "+texto);
      var url="https://wa.me/"+WA+"?text="+encodeURIComponent(lines.join("\n"));
      var w=window.open(url,"_blank","noopener");
      if(!w) location.href=url;
      msg.textContent="Abrimos o WhatsApp com a sua mensagem. É só tocar em enviar.";
    });
  }
  var y=$("year"); if(y) y.textContent=new Date().getFullYear();

  /* =========================================================
     HERÓI: folhagens do consultório em camadas + luz de janela
     ========================================================= */
  var scene=$("scene"), heroVisible=false, drawHero=null, applyParallax=null, sizeHero=null, scrollY=0;
  if(scene){
    heroVisible=true;
    var NS="http://www.w3.org/2000/svg", W=1600, H=900;
    var el=function(tag,attrs,parent){var e=d.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e;};
    var layer=function(depth){var svg=el("svg",{viewBox:"0 0 "+W+" "+H,preserveAspectRatio:"xMidYMid slice"});svg.dataset.depth=depth;scene.appendChild(svg);return svg;};
    /* folha simples com nervura central */
    var leaf=function(g,x,y,len,wid,ang,fill,vein){
      var t=el("g",{transform:"translate("+x+" "+y+") rotate("+ang+")"},g);
      el("path",{d:"M0 0 C "+(wid)+" "+(-len*.25)+" "+(wid*.9)+" "+(-len*.75)+" 0 "+(-len)+" C "+(-wid*.9)+" "+(-len*.75)+" "+(-wid)+" "+(-len*.25)+" 0 0Z",fill:fill},t);
      if(vein){
        el("path",{d:"M0 0 L0 "+(-len*.96),stroke:vein,"stroke-width":Math.max(1.2,wid/16),fill:"none"},t);
        for(var k=1;k<6;k++){var yy=-len*k/6.4;el("path",{d:"M0 "+yy+" q "+(wid*.4)+" "+(-len*.05)+" "+(wid*.72)+" "+(-len*.12)+" M0 "+yy+" q "+(-wid*.4)+" "+(-len*.05)+" "+(-wid*.72)+" "+(-len*.12),stroke:vein,"stroke-width":Math.max(.8,wid/30),fill:"none"},t);}
      }
    };
    /* ramo de samambaia */
    var fern=function(g,x,y,len,ang,color,r){
      var t=el("g",{transform:"translate("+x+" "+y+") rotate("+ang+")"},g);
      el("path",{d:"M0 0 Q "+(len*.12)+" "+(-len*.5)+" 0 "+(-len),stroke:color,"stroke-width":2,fill:"none"},t);
      for(var k=2;k<22;k++){
        var f=k/22, yy=-len*f, s=len*.16*(1-f*.8)+4, xx=Math.sin(f*Math.PI)*len*.06;
        leaf(t,xx,yy,s,s*.28,-62-r()*10,color,null);
        leaf(t,xx,yy,s,s*.28,62+r()*10,color,null);
      }
    };
    var specs=[
      {depth:.10, op:.22, seed:3, col:"#E6D6BC"},
      {depth:.25, op:.35, seed:11, col:"#C9AD89"},
      {depth:.45, op:.55, seed:29, col:"#8A5C3C"}
    ];
    var layers=[];
    var sun=d.createElement("div"); sun.className="sun"; scene.appendChild(sun);
    specs.forEach(function(s,i){
      var L=layer(s.depth), r=rnd(s.seed), g=el("g",{opacity:s.op},L);
      /* tufos nos cantos inferiores e na borda direita, longe do texto */
      var spots=[[0,H],[W,H],[W,H*.45],[W*.06,H*.92]];
      spots.forEach(function(p,j){
        if(i===2&&j===3) return;
        var n=4+Math.floor(r()*4);
        for(var k=0;k<n;k++){
          var len=140+r()*240-(2-i)*20, wid=len*(.22+r()*.12);
          var base=p[0]===0?-40+r()*80:(p[0]===W?-90+r()*40:-90+r()*60);
          var ang=p[0]===0?(10+r()*60):(-70+r()*60);
          if(r()<.3) fern(g,p[0]+(p[0]===0?r()*80:-r()*80),p[1]-r()*40,len*1.3,ang,s.col,r);
          else leaf(g,p[0]+(p[0]===0?r()*120:-r()*120),p[1]+r()*30,len,wid,ang+base*.1,s.col,i===2?"rgba(255,255,255,.18)":null);
        }
      });
      layers.push(L);
    });
    var cv=d.createElement("canvas"); scene.appendChild(cv);
    var ctx=cv.getContext("2d"), cw=0, ch=0;
    sizeHero=function(){cw=scene.clientWidth;ch=scene.clientHeight;cv.width=cw*dpr;cv.height=ch*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);};
    sizeHero();
    /* partículas de poeira na luz da janela */
    var R=rnd(99), motes=[];
    for(var f=0;f<38;f++) motes.push({x:.45+R()*.55,y:R(),vx:(R()-.5)*.00025,vy:-.00008-R()*.00018,p:R()*6.28,s:.8+R()*1.8});
    var mx=0,my=0,tx=0,ty=0;
    window.addEventListener("pointermove",function(e){tx=(e.clientX/window.innerWidth-.5);ty=(e.clientY/window.innerHeight-.5);},{passive:true});
    drawHero=function(t){
      ctx.clearRect(0,0,cw,ch);
      motes.forEach(function(q){
        q.x+=q.vx+Math.sin(t/2200+q.p)*.00012; q.y+=q.vy;
        if(q.y<-.02){q.y=1.02;q.x=.45+R()*.55;}
        var a=.35+.35*Math.sin(t/900+q.p*3);
        ctx.fillStyle="rgba(186,152,114,"+a.toFixed(3)+")";
        ctx.beginPath();ctx.arc(q.x*cw,q.y*ch,q.s,0,6.283);ctx.fill();
      });
    };
    applyParallax=function(){
      mx+=(tx-mx)*.05; my+=(ty-my)*.05;
      var sy=Math.min(scrollY,ch);
      for(var k=0;k<layers.length;k++){
        var dep=+layers[k].dataset.depth;
        layers[k].style.transform="translate3d("+(-mx*70*dep)+"px,"+(sy*dep*.5+(-my*24*dep))+"px,0)";
      }
    };
    new IntersectionObserver(function(es){heroVisible=es[0].isIntersecting;}).observe(scene.parentElement);
  }

  /* ---------- Folhas caindo nos escritos ---------- */
  var lc=$("leaves"), leavesVisible=false, drawLeaves=null, lsize=null;
  if(lc){
    var lx=lc.getContext("2d"), lw=0, lh=0, LR=rnd(17), leaves=[];
    lsize=function(){lw=lc.clientWidth;lh=lc.clientHeight;lc.width=lw*dpr;lc.height=lh*dpr;lx.setTransform(dpr,0,0,dpr,0,0);};
    lsize();
    var cols=["rgba(154,106,69,.32)","rgba(101,55,28,.26)","rgba(186,152,114,.42)"];
    for(var l=0;l<20;l++) leaves.push({x:LR(),y:LR(),s:7+LR()*10,sp:.00035+LR()*.0005,p:LR()*6.28,rot:LR()*6.28,c:cols[l%3]});
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

  /* ---------- Painel horizontal de temas ---------- */
  var temas=$("temas"), track=$("temasTrack"), bar=$("temasBar"), horizontal=false;
  function setupTemas(){
    if(!temas) return;
    horizontal=!reduce && window.innerWidth>760;
    if(!horizontal){temas.style.height="";track.style.transform="";return;}
    var extra=track.scrollWidth-window.innerWidth;
    temas.style.height=(window.innerHeight+Math.max(0,extra))+"px";
  }
  function updateTemas(){
    if(!temas||!horizontal) return;
    var r=temas.getBoundingClientRect(), total=temas.offsetHeight-window.innerHeight;
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

  /* ---------- Loop ---------- */
  function onScroll(){
    scrollY=window.scrollY||window.pageYOffset;
    if(head) head.classList.toggle("solid",scrollY>40);
    updateTemas(); updateTrail();
  }
  window.addEventListener("scroll",onScroll,{passive:true});
  window.addEventListener("resize",function(){sizeHero&&sizeHero();lsize&&lsize();setupTemas();setupTrail();onScroll();});
  setupTemas(); setupTrail(); onScroll();
  drawHero&&drawHero(0); drawLeaves&&drawLeaves(0); applyParallax&&applyParallax();
  if(!reduce){
    (function frame(t){
      if(heroVisible&&drawHero){drawHero(t);applyParallax();}
      if(leavesVisible&&drawLeaves) drawLeaves(t);
      requestAnimationFrame(frame);
    })(0);
  }
})();
