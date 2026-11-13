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
  /* ---------- Escritos em janela ---------- */
  d.querySelectorAll("[data-read]").forEach(function(card){
    var dlg=$(card.getAttribute("data-read")); if(!dlg||!dlg.showModal) return;
    var open=function(){dlg.showModal();};
    card.addEventListener("click",open);
    dlg.querySelector(".close").addEventListener("click",function(){dlg.close();});
    dlg.addEventListener("click",function(e){if(e.target===dlg) dlg.close();});
    dlg.addEventListener("close",function(){var b=card.querySelector(".go"); if(b) b.focus();});
  });
  var y=$("year"); if(y) y.textContent=new Date().getFullYear();

  /* =========================================================
     HERÓI: sempre-vivas da logo em camadas + sementes ao vento
     ========================================================= */
  var scene=$("scene"), heroVisible=false, drawHero=null, applyParallax=null, sizeHero=null, scrollY=0;
  if(scene){
    heroVisible=true;
    /* Sempre-vivas da logo em três camadas de profundidade (parallax), longe do texto */
    var specs=[
      {depth:.10, src:"img/flor-1.webp", items:[[90,58,28,-8],[-1,112,22,10],[72,110,20,4]]},
      {depth:.25, src:"img/flor-2.webp", items:[[97,40,34,6],[-5,118,28,-12],[58,118,18,-4]]},
      {depth:.45, src:"img/flor-3.webp", items:[[100,98,40,-4],[3,130,24,14]]}
    ];
    var layers=[];
    var sun=d.createElement("div"); sun.className="sun"; scene.appendChild(sun);
    specs.forEach(function(s){
      var L=d.createElement("div"); L.className="layer"; L.dataset.depth=s.depth; scene.appendChild(L);
      s.items.forEach(function(it,k){
        var im=d.createElement("img"); im.src=s.src; im.alt=""; im.decoding="async";
        im.style.cssText="left:"+it[0]+"%;top:"+it[1]+"%;height:"+it[2]+"vmax;--r:"+it[3]+"deg;--sw:"+(5+k*1.5)+"s";
        L.appendChild(im);
      });
      layers.push(L);
    });
    var cv=d.createElement("canvas"); scene.appendChild(cv);
    var ctx=cv.getContext("2d"), cw=0, ch=0;
    sizeHero=function(){cw=scene.clientWidth;ch=scene.clientHeight;cv.width=cw*dpr;cv.height=ch*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);};
    sizeHero();
    /* sementes da sempre-viva soltas no ar */
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
