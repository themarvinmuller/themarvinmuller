/* Taise Ferreira: interações simples (menu, revelação suave, glossário, escritos, formulário). */
(function(){
  "use strict";
  var d=document, root=d.documentElement;
  root.classList.add("js");
  var reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var WA="5562982226820";
  function $(id){return d.getElementById(id);}

  /* ---------- Links de WhatsApp ---------- */
  var waText="Olá, Taise! Vim pelo site e gostaria de marcar uma primeira conversa.";
  d.querySelectorAll("[data-wa]").forEach(function(a){
    a.href="https://wa.me/"+WA+"?text="+encodeURIComponent(waText); a.target="_blank"; a.rel="noopener";
  });

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

  /* ---------- Cabeçalho ---------- */
  function onScroll(){ if(head) head.classList.toggle("solid",(window.scrollY||window.pageYOffset)>40); }
  window.addEventListener("scroll",onScroll,{passive:true});
  onScroll();
})();
