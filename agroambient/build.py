#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o site estático da AgroAmbient em dist/.

Uso:  python3 build.py
Só usa a biblioteca padrão do Python, então roda igual na sua máquina e no build da Vercel.
Conteúdo em content.py, estilos em assets/site.css, scripts em assets/site.js, imagens em static/.
"""
import datetime
import hashlib
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

from content import SITE, PHOTOS, AREAS, SERVICES, GLOSS, FAQ, POSTS, PARTNERS, SECTORS, DIFERENCIAIS

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
U = SITE["url"].rstrip("/")
TODAY = datetime.date.today().isoformat()
SVC = {s["slug"]: s for s in SERVICES}
AREA_NAME = {a[0]: a[1] for a in AREAS}
AREA_ASSUNTO = {"fauna": "Estudos de fauna", "licenciamento": "Licenciamento e assessoria", "agro": "Agro e produção", "educacao": "Cursos e palestras"}
PAGES = []  # (path, title) para sitemap e llms

# ---------------------------------------------------------------------------
# utilidades
# ---------------------------------------------------------------------------
def e(s):
    return html.escape(str(s), quote=True)


TBD_RE = re.compile(r"\[\[(.+?)\]\]")


def tbd(s):
    """Texto com marcadores [[...]] -> HTML com etiqueta 'a confirmar'. O resto é escapado."""
    out, last = [], 0
    for m in TBD_RE.finditer(s):
        out.append(e(s[last:m.start()]))
        inner = m.group(1)
        if inner == "a confirmar":
            out.append('<span class="tbd-tag">a confirmar</span>')
        elif inner.endswith(", a confirmar"):
            out.append('<span class="tbd" title="A confirmar">%s</span> <span class="tbd-tag">a confirmar</span>' % e(inner[:-13]))
        else:
            out.append('<span class="tbd-tag" title="%s">a confirmar</span>' % e(inner))
        last = m.end()
    out.append(e(s[last:]))
    return "".join(out)


def plain(s):
    """Texto limpo (sem marcadores nem HTML) para meta tags, JSON-LD e llms.txt."""
    s = TBD_RE.sub(lambda m: m.group(1)[:-13] if m.group(1).endswith(", a confirmar") else "", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip().replace(" .", ".")


def file_hash(p):
    return hashlib.sha1(p.read_bytes()).hexdigest()[:10]


def abs_url(path):
    return U + path


def ld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


ORG_ID = U + "/#organizacao"
SITE_ID = U + "/#site"

LOGO_IMG = '<img src="/static/logo-agroambient.png" alt="" width="44" height="44">'
LOGO_SVG = '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="{bg}"/><path d="M20 31V15" stroke="#F4F1E4" stroke-width="2" stroke-linecap="round"/><path d="M20 22c-6 0-9-4-9-9 6 0 9 4 9 9zM20 18c5 0 8-3 8-8-5 0-8 3-8 8z" fill="#D99A12"/><path d="M9 30c4-2 8-2 11 0s7 2 11 0" stroke="#62B7C0" stroke-width="2" fill="none" stroke-linecap="round"/></svg>'
LEAF_DECO = '<svg class="deco" viewBox="0 0 200 200" aria-hidden="true"><path d="M100 190V60M100 120c-40 0-60-25-60-60 40 0 60 25 60 60zM100 95c35 0 52-22 52-52-35 0-52 22-52 52z" fill="currentColor"/></svg>'
ARROW = '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M3 9h12M10 4l5 5-5 5" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICONS = {
    "fauna": '<ellipse cx="26" cy="33" rx="9" ry="10"/><circle cx="13" cy="20" r="4"/><circle cx="21" cy="12" r="4"/><circle cx="31" cy="12" r="4"/><circle cx="39" cy="20" r="4"/>',
    "licenciamento": '<path d="M14 6h18l8 8v32H14z"/><path d="M32 6v8h8M20 24h14M20 31h14M20 38h8"/>',
    "agro": '<path d="M26 46V22"/><path d="M26 30c-9 0-14-6-14-14 9 0 14 6 14 14zM26 24c8 0 12-5 12-12-8 0-12 5-12 12z"/><path d="M8 46h36"/>',
    "educacao": '<path d="M6 18l20-9 20 9-20 9z"/><path d="M14 22v10c0 3 6 6 12 6s12-3 12-6V22M46 18v12"/>',
}


def icon(area):
    return '<svg class="svc-icon" viewBox="0 0 52 52" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICONS[area]


def photo(key, alt, cls="", caption=None, style=""):
    cap = '<figcaption>%s</figcaption>' % e(caption) if caption else ""
    return ('<figure class="photo %s" style="margin:0;%s"><img loading="lazy" decoding="async" src="%s" alt="%s">'
            '<span class="ph">%s</span>%s</figure>') % (cls, style, e(PHOTOS[key]), e(alt), e(caption or alt), cap)


def contato_href(assunto=None):
    return "/contato/" + ("?assunto=" + quote(assunto) if assunto else "")


# ---------------------------------------------------------------------------
# dados estruturados
# ---------------------------------------------------------------------------
def org_ld():
    o = {
        "@type": ["Organization", "ProfessionalService"],
        "@id": ORG_ID,
        "name": SITE["name"],
        "legalName": SITE["legal_name"],
        "alternateName": ["Agroambient", "AgroAmbient Assessoria Agro-Ambiental"],
        "url": U + "/",
        "logo": abs_url("/static/logo-agroambient.png"),
        "image": abs_url("/static/og.png"),
        "description": SITE["description"],
        "slogan": SITE["slogan"],
        "telephone": SITE["phone_e164"],
        "email": SITE["email"],
        "address": {"@type": "PostalAddress", "streetAddress": SITE["street"], "addressLocality": SITE["city"],
                    "addressRegion": SITE["region"], "postalCode": SITE["postal"], "addressCountry": "BR"},
        "geo": {"@type": "GeoCoordinates", "latitude": SITE["geo"][0], "longitude": SITE["geo"][1]},
        "areaServed": [{"@type": "Country", "name": "Brasil"}, {"@type": "State", "name": "Goiás"}, {"@type": "State", "name": "Minas Gerais"}],
        "founder": {"@type": "Person", "name": SITE["founder"], "jobTitle": SITE["founder_title"]},
        "foundingDate": SITE["founded"],
        "taxID": SITE["cnpj"],
        "identifier": [{"@type": "PropertyValue", "propertyID": "CNPJ", "value": SITE["cnpj"]},
                       {"@type": "PropertyValue", "propertyID": "CTF/IBAMA", "value": SITE["ctf"]},
                       {"@type": "PropertyValue", "propertyID": "CRBio-04", "value": SITE["crbio"]}],
        "knowsAbout": ["estudos de fauna", "monitoramento de fauna", "inventário de fauna", "resgate de fauna",
                       "ictiofauna", "transposição de peixes", "licenciamento ambiental", "outorga de água",
                       "EIA/RIMA", "PCA", "RAP", "PRAD", "PTRF", "PAE", "biota aquática", "ictioplâncton",
                       "necropsia de peixes", "laudos periciais ambientais", "manejo de macrófitas", "mapeamento com drone",
                       "educação ambiental", "Cerrado"],
        "sameAs": [x for x in [SITE["facebook"], SITE["instagram"]] if x],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Serviços ambientais",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": abs_url("/servicos/%s/" % s["slug"])}} for s in SERVICES]},
    }
    return o


def site_ld():
    return {"@type": "WebSite", "@id": SITE_ID, "url": U + "/", "name": SITE["name"], "inLanguage": "pt-BR", "publisher": {"@id": ORG_ID}}


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(p)} for i, (n, p) in enumerate(items)]}


def faq_ld(pairs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in pairs if plain(a)]}


# ---------------------------------------------------------------------------
# moldura da página
# ---------------------------------------------------------------------------
NAV = [("/sobre/", "Sobre"), ("/servicos/", "Serviços"), ("/fauna/", "Fauna"), ("/cursos-e-palestras/", "Cursos e palestras"),
       ("/projetos/", "Projetos"), ("/blog/", "Blog"), ("/contato/", "Contato")]


def tracking_script():
    cfg = json.dumps({"ga4": SITE["ga4"], "ads": SITE["ads"], "adsLeadLabel": SITE["ads_lead_label"]})
    return """<script>
window.AGRO_TRACKING=%s;
(function(){"use strict";var cfg=window.AGRO_TRACKING,KEY="agro-consent";window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}window.gtag=window.gtag||gtag;var stored=null;try{stored=localStorage.getItem(KEY);}catch(e){}var g=stored==="granted"?"granted":"denied";
gtag("consent","default",{ad_storage:g,ad_user_data:g,ad_personalization:g,analytics_storage:g,wait_for_update:500});
var primary=cfg.ga4||cfg.ads;if(primary){var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id="+encodeURIComponent(primary);document.head.appendChild(s);gtag("js",new Date());if(cfg.ga4)gtag("config",cfg.ga4);if(cfg.ads)gtag("config",cfg.ads);}
function ev(n,p){p=p||{};dataLayer.push(Object.assign({event:n},p));if(primary)gtag("event",n,p);}
window.agroTrack={event:ev,lead:function(a){ev("generate_lead",{assunto:a||""});if(cfg.ads&&cfg.adsLeadLabel)gtag("event","conversion",{send_to:cfg.ads+"/"+cfg.adsLeadLabel});},consent:function(ok){var v=ok?"granted":"denied";try{localStorage.setItem(KEY,v);}catch(e){}gtag("consent","update",{ad_storage:v,ad_user_data:v,ad_personalization:v,analytics_storage:v});},stored:stored};
document.addEventListener("click",function(e){var el=e.target.closest&&e.target.closest("[data-track]");if(el)ev(el.getAttribute("data-track"),{local:el.getAttribute("data-local")||location.pathname});});
document.addEventListener("DOMContentLoaded",function(){var b=document.getElementById("consent");if(!b)return;if(!stored&&primary)b.hidden=false;document.getElementById("consentYes").onclick=function(){agroTrack.consent(true);b.hidden=true;};document.getElementById("consentNo").onclick=function(){agroTrack.consent(false);b.hidden=true;};var o=document.getElementById("consentOpen");if(o)o.onclick=function(){b.hidden=false;};});
})();
</script>""" % cfg


def header(path):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if (path == href or (href != "/" and path.startswith(href))) else ""
        links.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    return """<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/" aria-label="AgroAmbient, página inicial">%s AgroAmbient</a>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="nav" aria-label="Abrir menu">
      <svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true"><path id="menuIcon" d="M4 9h20M4 19h20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    </button>
    <nav class="nav" id="nav" aria-label="Principal">
      %s
      <a class="btn btn-ipe" href="/contato/" data-track="cta_orcamento" data-local="menu">Solicitar orçamento</a>
    </nav>
  </div>
</header>""" % (LOGO_IMG, "\n      ".join(links))


def footer():
    svc_links = "".join('<li><a href="/servicos/%s/">%s</a></li>' % (s["slug"], e(s["name"])) for s in SERVICES[:7])
    wa = ("https://wa.me/%s?text=%s" % (SITE["whatsapp_e164"], quote("Olá! Vim pelo site da AgroAmbient."))) if SITE["whatsapp_e164"] else "/contato/"
    wa_label = "Falar pelo WhatsApp" if SITE["whatsapp_e164"] else "Falar com a AgroAmbient (WhatsApp a confirmar)"
    return """<footer class="site-foot">
  <div class="wrap">
    <div>
      <a class="brand" href="/" style="color:#F4F1E4">%s AgroAmbient</a>
      <p style="margin-top:1rem;max-width:40ch">Assessoria agroambiental e estudos de fauna terrestre e aquática. Base em Catalão (GO), atuação em todo o Brasil.</p>
      <p style="margin-top:1rem"><a href="%s" target="_blank" rel="noopener">Facebook</a></p>
    </div>
    <div><h4>Serviços</h4><ul>%s<li><a href="/servicos/">Todos os serviços</a></li></ul></div>
    <div><h4>Contato</h4><ul><li><a href="tel:%s" data-track="phone_click">%s</a></li><li>%s</li><li>%s</li><li>%s, %s · %s</li><li><a href="/perguntas-frequentes/">Perguntas frequentes</a></li><li><a href="/blog/">Blog</a></li></ul></div>
    <div class="legal"><span>© <span id="year">%s</span> %s · <a href="/politica-de-privacidade/">Privacidade</a> · <button class="consent-link" type="button" id="consentOpen">Preferências de cookies</button></span><span>CNPJ %s · CTF/IBAMA %s · CRBio-04 %s</span></div>
  </div>
</footer>
<div class="consent" id="consent" role="dialog" aria-live="polite" aria-label="Preferências de cookies" hidden>
  <div><strong>Cookies e medição</strong><p>Usamos cookies do Google Analytics e do Google Ads para entender as visitas e melhorar nossos anúncios. Veja a <a href="/politica-de-privacidade/">política de privacidade</a>.</p></div>
  <div class="row"><button class="btn btn-ipe" type="button" id="consentYes">Aceitar</button><button class="btn btn-line" type="button" id="consentNo">Recusar</button></div>
</div>
<a class="wa" href="%s" id="waBtn" data-track="whatsapp_click" aria-label="%s"%s>
  <svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.7 3.7 0 0 0-1.1 2.7 6.4 6.4 0 0 0 1.3 3.4 14.7 14.7 0 0 0 5.7 5c2.1.9 2.9 1 4 .8.6-.1 1.9-.8 2.2-1.5s.3-1.4.2-1.5-.3-.2-.6-.3z"/></svg>
</a>""" % (LOGO_IMG, SITE["facebook"], svc_links, SITE["phone_e164"], SITE["phone"], SITE["email"],
           SITE["street"], SITE["city"], SITE["region"], SITE["postal"], datetime.date.today().year, SITE["legal_name"], SITE["cnpj"], SITE["ctf"], SITE["crbio"],
           wa, wa_label, ' target="_blank" rel="noopener"' if SITE["whatsapp_e164"] else "")


ASSET_V = {}


def render(path, title, description, body, schema=(), og_type="website", noindex=False, extra_head=""):
    """Escreve dist/<path>/index.html."""
    full_title = title if "AgroAmbient" in title else "%s | AgroAmbient" % title
    graph = {"@context": "https://schema.org", "@graph": [org_ld() if path == "/" else {"@id": ORG_ID, "@type": ["Organization", "ProfessionalService"], "name": SITE["name"], "url": U + "/"},
                                                          site_ld()] + list(schema)}
    canon = abs_url(path)
    desc = plain(description)
    verify = '<meta name="google-site-verification" content="%s">\n' % e(SITE["gsc_verification"]) if SITE["gsc_verification"] else ""
    doc = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="AgroAmbient">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#13201A">
<meta name="geo.region" content="BR-GO">
<meta name="geo.placename" content="Catalão">
{verify}<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/static/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/static/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="alternate" type="text/plain" title="Resumo para assistentes de IA" href="/llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800&family=Figtree:ital,wght@0,400..700;1,400..600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/site.css?v={vcss}">
{tracking}
{extra}{ld}
<style>:root{{padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>
</head>
<body>
{header}
<main id="conteudo">
{body}
</main>
{footer}
<script src="/assets/site.js?v={vjs}" defer></script>
</body>
</html>
""".format(title=e(full_title), desc=e(desc), canon=canon, robots="noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1",
           og_type=og_type, og=abs_url("/static/og.png"), verify=verify, vcss=ASSET_V["css"], vjs=ASSET_V["js"],
           tracking=tracking_script(), extra=extra_head, ld=ld(graph), header=header(path), body=body, footer=footer())
    out = DIST / path.strip("/") / "index.html" if path != "/404" else DIST / "404.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    if not noindex:
        PAGES.append((path, full_title, desc))


# ---------------------------------------------------------------------------
# blocos reutilizáveis
# ---------------------------------------------------------------------------
def crumbs_html(items, dark=True):
    lis = "".join('<li><a href="%s">%s</a></li>' % (p, e(n)) if i < len(items) - 1 else '<li aria-current="page">%s</li>' % e(n)
                  for i, (n, p) in enumerate(items))
    return '<nav aria-label="Você está em"><ol class="crumbs">%s</ol></nav>' % lis


def hero_page(title, lede, crumbs, eyebrow="", seed=1, kind="cerrado", ctas=None, meta=""):
    ctas_html = ""
    if ctas:
        ctas_html = '<div class="ctas fade-in" style="--d:.3s">%s</div>' % "".join(ctas)
    eb = '<p class="eyebrow fade-in">%s</p>' % e(eyebrow) if eyebrow else ""
    if kind == "river":
        return """<section class="river page-river" aria-label="Apresentação">
  <canvas id="riverCanvas" aria-hidden="true"></canvas>
  <div class="wrap">%s%s<h1>%s</h1><p class="lede">%s</p>%s%s</div>
</section>""" % (crumbs_html(crumbs), eb, e(title), tbd(lede), meta, ctas_html)
    return """<section class="hero hero-sm" aria-label="Apresentação">
  <div class="hero-scene" id="scene" data-seed="%d" aria-hidden="true"></div>
  <div class="wrap">%s%s<h1 id="heroTitle">%s</h1><p class="lede fade-in" style="--d:.15s">%s</p>%s%s</div>
</section>""" % (seed, crumbs_html(crumbs), eb, e(title), tbd(lede), meta, ctas_html)


def btn(href, label, cls="btn-ipe", track=None, local=None):
    t = ' data-track="%s"' % track if track else ""
    l = ' data-local="%s"' % local if local else ""
    arrow = ARROW if cls == "btn-ipe" else ""
    return '<a class="btn %s" href="%s"%s%s>%s %s</a>' % (cls, href, t, l, e(label), arrow)


def cta_band(title="Conte o que o seu empreendimento precisa.", text="Respondemos com uma proposta e os próximos passos.", assunto=None):
    return """<section class="sec" style="padding-top:0"><div class="wrap"><div class="cta-band reveal">%s
  <div><h2>%s</h2><p>%s</p></div>
  <div class="row">%s<a class="btn btn-line" style="color:inherit;box-shadow:inset 0 0 0 1.5px currentColor" href="tel:%s" data-track="phone_click">%s</a></div>
</div></div></section>""" % (LEAF_DECO, e(title), e(text), btn(contato_href(assunto), "Solicitar orçamento", track="cta_orcamento", local="faixa"), SITE["phone_e164"], SITE["phone"])


def svc_card(s):
    return '<a class="card reveal" href="/servicos/%s/"><p class="eyebrow">%s</p><h3>%s</h3><p>%s</p><span class="go">Ver serviço</span></a>' % (
        s["slug"], e(AREA_NAME[s["area"]]), e(s["name"]), e(s["short"]))


def post_card(p):
    d = datetime.date.fromisoformat(p["date"])
    return '<a class="card reveal" href="/blog/%s/"><p class="eyebrow"><time datetime="%s">%s</time></p><h3>%s</h3><p>%s</p><span class="go">Ler artigo</span></a>' % (
        p["slug"], p["date"], d.strftime("%d/%m/%Y"), e(p["title"]), e(p["description"]))


def faq_html(pairs):
    return '<div class="faq">%s</div>' % "".join(
        '<details><summary>%s</summary><div class="a"><p>%s</p></div></details>' % (e(q), tbd(a)) for q, a in pairs)


def areas_grid(with_links=True):
    out = []
    for i, (key, name, desc) in enumerate(AREAS):
        items = [s for s in SERVICES if s["area"] == key]
        lis = "".join('<li><a href="/servicos/%s/">%s</a></li>' % (s["slug"], e(s["name"])) for s in items)
        if key == "educacao":
            lis += '<li><a href="/cursos-e-palestras/">Cursos e palestras</a></li>'
        out.append('<article class="svc reveal" style="--d:%.2fs">%s<h3>%s</h3><p>%s</p><ul>%s</ul></article>' % (
            (i % 2) * .1, icon(key), e(name), e(desc), lis))
    return '<div class="svc-grid">%s</div>' % "".join(out)


def glossary():
    return """<div class="gloss reveal">
  <h3>O que significa cada sigla?</h3>
  <p>Toque em uma sigla para ver o que ela é e quando o órgão ambiental costuma pedir.</p>
  <div class="chips" role="group" aria-label="Siglas do licenciamento" id="chips"></div>
  <div class="chip-out" id="chipOut" aria-live="polite"><noscript>%s</noscript></div>
</div>
<script>window.AGRO_GLOSS=%s;</script>""" % (" · ".join(e(g[0] + ": " + g[1]) for g in GLOSS), json.dumps(GLOSS, ensure_ascii=False))


def process_html():
    steps = [
        ("Diagnóstico e escopo", "Entendemos o empreendimento, a exigência do órgão ambiental e o prazo. Você recebe uma proposta com o que será feito e quanto custa."),
        ("Planejamento e autorizações", "Definimos as campanhas, os métodos e a equipe, e solicitamos as autorizações de captura e manejo de fauna quando necessárias."),
        ("Campanhas de campo", "Equipe técnica em campo para coleta, registro e, quando é o caso, resgate e soltura dos animais."),
        ("Análise e relatório técnico", "Identificação das espécies, análise dos dados e relatório no formato pedido pelo órgão, com responsável técnico."),
        ("Protocolo e acompanhamento", "Protocolamos o estudo e acompanhamos o processo até a resposta do órgão, incluindo pedidos de informação complementar."),
    ]
    lis = "".join('<li class="step"><span class="n">%02d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i + 1, e(t), e(d)) for i, (t, d) in enumerate(steps))
    return """<section class="sec" id="processo"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Como trabalhamos</p><h2>Cinco etapas, do primeiro contato ao relatório aprovado.</h2></div>
  <div class="process-wrap" id="processWrap">
    <svg class="trail" id="trail" aria-hidden="true" preserveAspectRatio="none"><path class="bg" id="trailBg"/><path class="fg" id="trailFg"/></svg>
    <ol class="steps">%s</ol>
  </div>
</div></section>""" % lis


FAUNA_GROUPS = [
    ("fc-masto", "Mamíferos", "Mastofauna", "Armadilhas fotográficas, busca ativa, vestígios e pegadas para registrar mamíferos de pequeno a grande porte.",
     [("Chrysocyon brachyurus", "lobo-guará"), ("Myrmecophaga tridactyla", "tamanduá-bandeira"), ("Tapirus terrestris", "anta")], "Masto"),
    ("fc-avi", "Aves", "Avifauna", "Pontos de escuta, transectos e gravação de vocalizações para levantar a riqueza de aves da área.",
     [("Ara ararauna", "arara-canindé"), ("Cariama cristata", "seriema"), ("Rhea americana", "ema")], "Avi"),
    ("fc-herp", "Répteis e anfíbios", "Herpetofauna", "Busca ativa noturna, armadilhas de interceptação e queda e registro em sítios reprodutivos.",
     [("Caiman latirostris", "jacaré-de-papo-amarelo"), ("Salvator merianae", "teiú"), ("Rhinella diptycha", "sapo-cururu")], "Herpeto"),
    ("fc-ictio", "Peixes", "Ictiofauna", "Redes, tarrafas e outros métodos autorizados, com identificação taxonômica e análise ecológica das comunidades.",
     [("Salminus brasiliensis", "dourado"), ("Prochilodus lineatus", "curimbatá"), ("Pseudoplatystoma corruscans", "pintado")], "Ictio"),
]


def fauna_panel(heading_tag="h2"):
    cards = []
    for cls, kind, name, text, spp, big in FAUNA_GROUPS:
        dl = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in spp)
        cards.append('<article class="fcard %s"><div><p class="kind">%s</p><h3>%s</h3><p style="margin-top:.6rem">%s</p></div><dl>%s</dl><span class="big" aria-hidden="true">%s</span></article>' % (
            cls, e(kind), e(name), e(text), dl, big))
    return """<section class="fauna" id="fauna" aria-label="Grupos de fauna">
  <div class="fauna-pin">
    <div class="wrap fauna-head"><p class="eyebrow">Grupos que estudamos</p><%s style="font-size:var(--step-3);font-variation-settings:'wdth' 85;margin-top:.6rem">Quatro grupos, um mesmo rigor de campo.</%s></div>
    <div class="fauna-track" id="faunaTrack">%s</div>
    <div class="wrap"><div class="fauna-progress" aria-hidden="true"><i id="faunaBar"></i></div><p class="fauna-note">Espécies citadas como exemplos da fauna do Cerrado, não como registros de projetos.</p></div>
  </div>
</section>""" % (heading_tag, heading_tag, "".join(cards))


def river_block(title="Debaixo d’água também tem estudo.", link=True):
    more = '<p class="reveal" style="margin-top:2rem"><a class="btn btn-ghost" href="/servicos/estudos-ictiologicos/">Conhecer os estudos ictiológicos</a></p>' if link else ""
    return """<section class="river" id="rio" aria-label="Fauna aquática">
  <canvas id="riverCanvas" aria-hidden="true"></canvas>
  <div class="wrap">
    <p class="eyebrow reveal">Fauna aquática</p>
    <h2 class="reveal">%s</h2>
    <p class="lede reveal">Coleta, identificação e monitoramento da ictiofauna em rios, reservatórios e barramentos. Planejamos e executamos resgates durante obras e operações de transposição de peixes, com especialistas em ecologia e taxonomia.</p>
    <div class="river-list reveal"><a href="/servicos/estudos-ictiologicos/"><span>Estudos ictiológicos</span></a><a href="/servicos/resgate-de-fauna/"><span>Resgate de ictiofauna</span></a><a href="/servicos/transposicao-de-peixes/"><span>Transposição de peixes</span></a></div>
    %s<small class="reveal">PASSE O MOUSE OU O DEDO NA ÁGUA</small>
  </div>
</section>""" % (e(title), more)


ASSUNTOS = ["Estudos de fauna", "Licenciamento e assessoria", "Agro e produção", "Cursos e palestras", "Parcerias", "Trabalhe conosco"]


def contact_block(heading="h2", title="Conte o que o seu empreendimento precisa."):
    opts = "".join('<option>%s</option>' % e(a) for a in ASSUNTOS)
    wa = ('<a href="https://wa.me/%s" target="_blank" rel="noopener" data-track="whatsapp_click">%s</a>' % (SITE["whatsapp_e164"], SITE["whatsapp"])) if SITE["whatsapp_e164"] else \
        ""
    insta = (' · <a href="%s" target="_blank" rel="noopener">Instagram</a>' % SITE["instagram"]) if SITE["instagram"] else ""
    if SITE["whatsapp_e164"]:
        intro, btn = "Preencha em 30 segundos. Ao enviar, o WhatsApp abre com a mensagem pronta para a nossa equipe.", "Enviar pelo WhatsApp"
    else:
        intro, btn = "Preencha em 30 segundos. Ao enviar, seu e-mail abre com a mensagem pronta para a nossa equipe.", "Enviar pedido"
    maps = "https://www.google.com/maps/search/?api=1&query=" + quote("%s, %s - %s, %s" % (SITE["street"], SITE["city"], SITE["region"], SITE["postal"]))
    return """<div class="contact-grid">
  <div class="cinfo reveal">
    <dl>
      <div><dt>Telefone</dt><dd><a id="tel" href="tel:%s" data-track="phone_click">%s</a><button class="copy" type="button" data-copy="tel" data-track="copy_phone">copiar</button></dd></div>
      <div><dt>WhatsApp</dt><dd>%s</dd></div>
      <div><dt>E-mail</dt><dd><span id="mail">%s</span><button class="copy" type="button" data-copy="mail" data-track="copy_email">copiar</button></dd></div>
      <div><dt>Endereço</dt><dd>%s<br>%s, %s · %s<br><a href="%s" target="_blank" rel="noopener" style="font-size:.92rem;font-weight:500">Ver no Google Maps</a></dd></div>
      <div><dt>Redes</dt><dd><a href="%s" target="_blank" rel="noopener">Facebook</a>%s</dd></div>
    </dl>
  </div>
  <form id="form" class="reveal" style="--d:.1s" novalidate data-wa="%s" data-email="%s" aria-label="Pedido de orçamento pelo WhatsApp">
    <p class="form-intro">%s</p>
    <div class="row2">
      <label for="f-nome">Seu nome<input id="f-nome" name="nome" autocomplete="name" required></label>
      <label for="f-cidade">Cidade do empreendimento<input id="f-cidade" name="cidade" placeholder="Ex.: Catalão, GO"></label>
    </div>
    <label for="f-assunto">Do que você precisa?<select id="f-assunto" name="assunto">%s</select></label>
    <label for="f-msg">Conte em poucas palavras <span style="font-weight:400;color:var(--muted)">(opcional)</span><textarea id="f-msg" name="mensagem" rows="3" placeholder="Tipo de empreendimento, o que o órgão pediu, prazo..."></textarea></label>
    <p style="font-size:.82rem;color:var(--muted)">Usamos seus dados só para responder ao pedido. Veja a <a href="/politica-de-privacidade/">política de privacidade</a>.</p>
    <div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:center">
      <button class="btn btn-ipe btn-wa" type="submit"><svg aria-hidden="true" viewBox="0 0 32 32" width="20" height="20"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.5-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.6.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.8 5 2.1.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.2-.6-.4z"/></svg> %s</button>
      <p class="form-msg" id="formMsg" aria-live="polite"></p>
    </div>
  </form>
</div>""" % (SITE["phone_e164"], SITE["phone"], wa, SITE["email"], SITE["street"], SITE["city"], SITE["region"], SITE["postal"], maps,
           SITE["facebook"], insta, SITE["whatsapp_e164"], SITE["email"], intro, opts, btn)


def portfolio_btn(local, cls="btn-line"):
    return '<a class="btn %s" href="%s" download data-track="download_portfolio" data-local="%s">Baixar portfólio (PDF)</a>' % (cls, SITE["portfolio_pdf"], local)


def partners_html():
    return '<ul class="partners">%s</ul>' % "".join('<li>%s</li>' % e(x) for x in PARTNERS)


def credentials_html():
    items = [("Fundada em", SITE["founded"]), ("CNPJ", SITE["cnpj"]), ("CTF/IBAMA", SITE["ctf"]), ("CRBio-04", SITE["crbio"])]
    return '<dl class="creds reveal">%s</dl>' % "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in items)


def gallery():
    items = [("monitoramento", "Armadilha fotográfica", "g1"), ("ictio", "Ictiofauna em reservatório", "g2"), ("resgate", "Resgate de fauna", "g3"),
             ("macrofitas", "Manejo de macrófitas", "g4"), ("eia", "Levantamento para EIA/RIMA", "g5"), ("drone", "Mapeamento com drone", "g6")]
    return '<div class="gallery">%s</div>' % "".join(
        photo(k, "Registro de campo da AgroAmbient: " + c.lower(), cls=g + " reveal", caption=c, style="--d:%.2fs" % ((i % 3) * .08)) for i, (k, c, g) in enumerate(items))


# ---------------------------------------------------------------------------
# páginas
# ---------------------------------------------------------------------------
def page_home():
    faq_preview = [FAQ[1][1][0], FAQ[2][1][0], FAQ[3][1][0], FAQ[0][1][1]]
    body = """<section class="hero" id="inicio" aria-label="Apresentação">
  <div class="hero-scene" id="scene" data-seed="1" aria-hidden="true"></div>
  <div class="wrap">
    <p class="eyebrow fade-in">Consultoria ambiental · Fauna terrestre e aquática</p>
    <h1 id="heroTitle">Preservação ambiental, <em>plante esta ideia.</em></h1>
    <p class="lede fade-in" style="--d:.15s">Estudos de fauna, licenciamento e assessoria agroambiental em todo o Brasil, a partir de Catalão, em Goiás, na divisa com Minas Gerais.</p>
    <div class="ctas fade-in" style="--d:.3s">%s<a class="btn btn-ghost" href="/servicos/">Conhecer os serviços</a></div>
  </div>
  <p class="coords" aria-hidden="true">CATALÃO · GO<br>18°10′S 47°57′W</p>
  <span class="scroll-hint" aria-hidden="true"></span>
</section>

<section class="sec" id="sobre"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">A empresa</p><h2>Consultoria ambiental especializada em fauna.</h2>
    <p>A AgroAmbient é especializada em estudos de fauna e oferece assessoria ambiental e agrícola completa em todo o território nacional, com profissionais qualificados.</p></div>
  <div class="about-grid">
    <div class="about-text reveal">
      <p>Fundada em 2015, a AgroAmbient atua com fauna terrestre e aquática: monitoramento, inventariamento, resgate, biota aquática e ictioplâncton, laudos e necropsia, sempre com biólogos especialistas nas diversas áreas da zoologia. Junto disso, cuidamos da parte técnica e documental que o empreendimento precisa para operar dentro da lei.</p>
      <p>Atendemos empresas de consultoria e gestão ambiental e os setores minerário, energético, agropecuário e industrial.</p>
      <p>A empresa também ministra cursos e palestras para instruir a sociedade a respeito da preservação ambiental, aliada ao desenvolvimento econômico e sustentável.</p>
      <p style="display:flex;flex-wrap:wrap;gap:.8rem"><a class="btn btn-line" href="/sobre/">Conheça a AgroAmbient</a>%s</p>
      <div class="about-photos">%s%s%s</div>
    </div>
    <blockquote class="reveal" style="--d:.15s">
      <svg viewBox="0 0 200 200" aria-hidden="true"><path d="M100 190V60M100 120c-40 0-60-25-60-60 40 0 60 25 60 60zM100 95c35 0 52-22 52-52-35 0-52 22-52 52z" fill="currentColor"/></svg>
      <p>“A AgroAmbient surgiu de um sonho de aliar produtividade com preservação ambiental. É possível alimentar o mundo e, ao mesmo tempo, proteger a qualidade de vida.”</p>
      <footer>%s · %s</footer>
    </blockquote>
  </div>
</div></section>

<section class="sec" id="parceiros" style="padding-top:0"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Clientes e parceiros</p><h2>Quem já trabalhou com a gente.</h2></div>
  %s
</div></section>

<section class="sec services" id="servicos"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Serviços</p><h2>Do levantamento em campo ao protocolo no órgão ambiental.</h2>
    <p>Quatro frentes de trabalho que se complementam. Você pode contratar um estudo pontual ou a assessoria completa do empreendimento.</p></div>
  <div style="margin-top:3.5rem">%s</div>
  %s
</div></section>

%s
%s
%s

<section class="sec" id="campo" style="padding-top:0"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Do campo</p><h2>Registros reais dos nossos trabalhos.</h2></div>
  <div style="margin-top:3rem">%s</div>
</div></section>

<section class="sec courses" id="cursos">
  <canvas class="leaves" id="leaves" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Cursos e palestras</p><h2>Conhecimento que vai além do relatório.</h2>
      <p>Levamos a preservação ambiental para escolas, empresas, cooperativas e eventos do agro, sempre ligada ao desenvolvimento econômico e sustentável.</p></div>
    %s
  </div>
</section>

<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Perguntas frequentes</p><h2>Respostas rápidas para quem está começando.</h2></div>
  <div style="margin-top:2.4rem">%s</div>
  <p class="reveal" style="margin-top:1.6rem"><a class="btn btn-line" href="/perguntas-frequentes/">Ver todas as perguntas</a></p>
</div></section>

<section class="sec services"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Blog</p><h2>Guias sobre fauna e licenciamento.</h2></div>
  <div class="cards" style="margin-top:2.4rem">%s</div>
</div></section>

<section class="sec" id="contato"><div class="wrap">
  <div class="sec-head reveal"><p class="eyebrow">Contato</p><h2>Conte o que o seu empreendimento precisa.</h2><p>Respondemos com uma proposta e os próximos passos. Se preferir, fale direto pelo telefone.</p></div>
  <div style="margin-top:3rem">%s</div>
</div></section>""" % (
        btn("/contato/", "Solicitar orçamento", track="cta_orcamento", local="hero"),
        portfolio_btn("home"),
        photo("equipe", "Biólogo da AgroAmbient com puçá em levantamento de fauna no Cerrado", caption="Equipe em campo"),
        photo("monitoramento", "Instalação de armadilha fotográfica para monitoramento de fauna", caption="Armadilha fotográfica"),
        photo("necropsia", "Análise de peixes em laboratório com estereomicroscópio", caption="Laboratório"),
        e(SITE["founder"]), e(SITE["founder_title"]), partners_html(), areas_grid(), glossary(), river_block(), fauna_panel(), process_html(), gallery(),
        courses_cards() + '<p class="reveal" style="margin-top:2rem">%s</p>' % btn("/cursos-e-palestras/", "Ver cursos e palestras"),
        faq_html(faq_preview), "".join(post_card(p) for p in POSTS), contact_block())
    render("/", "AgroAmbient | Consultoria ambiental e estudos de fauna em Goiás, Minas e todo o Brasil",
           "Estudos de fauna terrestre e aquática, licenciamento ambiental, outorga e assessoria agroambiental em todo o Brasil, a partir de Catalão (GO).",
           body)


def courses_cards():
    items = [("Palestra", "Fauna do Cerrado e convivência no campo", "Como reconhecer, respeitar e conviver com a fauna nativa nas propriedades rurais."),
             ("Curso", "Manejo e resgate de fauna", "Boas práticas para equipes que atuam em obras, supressão de vegetação e reservatórios."),
             ("Programa", "Educação ambiental nas escolas", "Atividades adaptadas por idade, com saídas de campo e material de apoio.")]
    cards = "".join('<article class="course reveal" style="--d:%.2fs"><p class="eyebrow">%s</p><h3>%s</h3><p>%s</p></article>' % (i * .08, e(a), e(b), e(c)) for i, (a, b, c) in enumerate(items))
    return '<div class="course-grid">%s</div><p class="reveal" style="margin-top:1.6rem;color:rgba(244,241,228,.6);font-size:.9rem">Temas e formatos ajustados ao público de cada instituição.</p>' % cards


def page_sobre():
    cr = [("Início", "/"), ("Sobre", "/sobre/")]
    body = hero_page("Uma consultoria ambiental nascida no campo.", "Desde 2015, unimos estudos de fauna terrestre e aquática, assessoria ambiental e agrícola para empreendimentos em todo o Brasil.",
                     cr, eyebrow="Sobre a AgroAmbient", seed=3) + """
<section class="sec"><div class="wrap stack-lg">
  <div class="split">
    <div class="prose reveal">
      <h2 style="margin-top:0">Quem somos</h2>
      <p>Fundada em 2015, a AgroAmbient é especializada na execução de estudos e serviços ambientais voltados à fauna terrestre e aquática, e fornece assessoria ambiental e agrícola completa em todo o território nacional.</p>
      <p>Desenvolvemos soluções ambientais para empresas de consultoria e gestão ambiental e para os setores minerário, energético, agropecuário e industrial, com atendimento técnico em todas as etapas dos projetos, de forma eficiente, segura e alinhada às exigências legais.</p>
      <p>Nossa sede fica em Catalão, no sudeste de Goiás, na divisa com Minas Gerais, uma região de forte produção agrícola, mineração e Cerrado. Essa origem explica o jeito de trabalhar: entender a rotina de quem produz e encontrar o caminho para que a atividade cresça dentro da lei e com respeito ao ambiente.</p>
      <p>Além dos estudos técnicos, a AgroAmbient ministra cursos e palestras para instruir a sociedade a respeito da preservação ambiental, aliada ao desenvolvimento econômico e sustentável.</p>
    </div>
    <div class="reveal">%s</div>
  </div>
  <div class="values reveal">
    <div><h3>Missão</h3><p>Oferecer produtos, soluções e a execução de trabalhos de qualidade aos nossos clientes, auxiliando no crescimento profissional e pessoal de todos, aliando produtividade, eficiência e preservação do meio ambiente.</p></div>
    <div><h3>Visão</h3><p>Mostrar que produtividade e preservação ambiental andam juntas: é possível alimentar o mundo e, ao mesmo tempo, proteger a qualidade de vida.</p></div>
    <div><h3>Como trabalhamos</h3><p>Rigor técnico em campo, linguagem clara com o cliente e relatórios que respondem exatamente ao que o órgão ambiental pediu.</p></div>
  </div>
  <blockquote class="reveal">
    <svg viewBox="0 0 200 200" aria-hidden="true"><path d="M100 190V60M100 120c-40 0-60-25-60-60 40 0 60 25 60 60zM100 95c35 0 52-22 52-52-35 0-52 22-52 52z" fill="currentColor"/></svg>
    <p>“A AgroAmbient surgiu de um sonho de aliar produtividade com preservação ambiental.”</p>
    <footer>%s · %s</footer>
  </blockquote>
  <div>
    <div class="sec-head reveal"><p class="eyebrow">Equipe</p><h2>Profissionais qualificados em cada grupo de fauna.</h2>
      <p>Equipe multidisciplinar de biólogos especialistas nas diversas áreas da zoologia e da gestão ambiental, sob a direção do biólogo %s, mestre e especialista em Zoologia com ênfase em ictiofauna. Cada estudo tem responsável técnico habilitado.</p></div>
  </div>
  <div>
    <div class="sec-head reveal"><p class="eyebrow">Diferenciais</p><h2>O que você pode esperar da AgroAmbient.</h2></div>
    <ul class="checks reveal">%s</ul>
  </div>
  <div>
    <div class="sec-head reveal"><p class="eyebrow">Registros</p><h2>Empresa regularizada para trabalhar com fauna.</h2></div>
    %s
    <p class="reveal" style="margin-top:1.6rem">%s</p>
  </div>
  <div>
    <div class="sec-head reveal"><p class="eyebrow">Onde atuamos</p><h2>Base em Goiás, atuação em todo o Brasil.</h2>
      <p>De Catalão atendemos com frequência Goiás, o Triângulo Mineiro e o Alto Paranaíba, e deslocamos a equipe para projetos em qualquer estado.</p></div>
  </div>
</div></section>
%s""" % (photo("equipe", "Biólogo da AgroAmbient com puçá em levantamento de fauna no Cerrado", caption="Equipe em campo"), e(SITE["founder"]), e(SITE["founder_title"]),
         e(SITE["founder"]), "".join("<li>%s</li>" % e(d) for d in DIFERENCIAIS), credentials_html(), portfolio_btn("sobre", "btn-ipe"), cta_band())
    render("/sobre/", "Sobre a AgroAmbient: consultoria ambiental especializada em fauna",
           "Conheça a AgroAmbient, fundada em 2015 e especializada em estudos de fauna terrestre e aquática. Equipe de biólogos, registros no IBAMA e CRBio, missão e diferenciais.",
           body, schema=[{"@type": "AboutPage", "url": abs_url("/sobre/"), "name": "Sobre a AgroAmbient", "about": {"@id": ORG_ID}}, crumbs_ld(cr)])


def page_servicos():
    cr = [("Início", "/"), ("Serviços", "/servicos/")]
    sections = []
    for key, name, desc in AREAS:
        items = [s for s in SERVICES if s["area"] == key]
        cards = "".join(svc_card(s) for s in items)
        if key == "educacao":
            cards += '<a class="card reveal" href="/cursos-e-palestras/"><p class="eyebrow">Educação ambiental</p><h3>Cursos e palestras</h3><p>Formação para escolas, empresas, produtores e equipes de obra.</p><span class="go">Ver cursos</span></a>'
        sections.append('<div><div class="sec-head reveal" style="margin-bottom:1.6rem">%s<h2 style="font-size:var(--step-2)">%s</h2><p>%s</p></div><div class="cards">%s</div></div>' % (
            icon(key), e(name), e(desc), cards))
    body = hero_page("Serviços ambientais do campo ao órgão ambiental.", "Estudos de fauna, licenciamento, outorga, planos e programas ambientais, assessoria agrícola e educação ambiental.",
                     cr, eyebrow="Serviços", seed=5) + """
<section class="sec"><div class="wrap stack-lg">%s
  <div>%s</div>
</div></section>
%s
%s""" % ("".join(sections), glossary(), process_html(), cta_band())
    il = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": abs_url("/servicos/%s/" % s["slug"]), "name": s["name"]} for i, s in enumerate(SERVICES)]}
    render("/servicos/", "Serviços ambientais: fauna, licenciamento e outorga",
           "Monitoramento, inventário e resgate de fauna, estudos ictiológicos, licenciamento ambiental, outorga de água, EIA/RIMA, PRAD, PTRF e educação ambiental.",
           body, schema=[il, crumbs_ld(cr)])


def page_service(s):
    path = "/servicos/%s/" % s["slug"]
    cr = [("Início", "/"), ("Serviços", "/servicos/"), (s["name"], path)]
    assunto = AREA_ASSUNTO[s["area"]]
    ctas = [btn(contato_href(assunto), "Pedir orçamento", track="cta_orcamento", local=s["slug"])]
    hero = hero_page(s["title"], s["short"], cr, eyebrow=AREA_NAME[s["area"]], seed=7 + SERVICES.index(s), kind=s["hero"], ctas=ctas)
    parts = ['<div class="summary reveal"><span class="label">Em resumo</span><p>%s</p></div>' % tbd(s["summary"])]
    parts += ['<p>%s</p>' % tbd(p) for p in s["intro"]]
    if s.get("table"):
        rows = "".join('<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td></tr>' % (e(a), e(b), e(c)) for a, b, c in s["table"])
        parts.append('<div class="table-wrap"><table><thead><tr><th>Sigla</th><th>Nome</th><th>Quando é pedido</th></tr></thead><tbody>%s</tbody></table></div>' % rows)
    parts.append('<h2>Quando é necessário</h2><ul>%s</ul>' % "".join('<li>%s</li>' % tbd(w) for w in s["when"]))
    parts.append('<h2>Como fazemos</h2><ol class="howto">%s</ol>' % "".join('<li><div><strong>%s</strong><p>%s</p></div></li>' % (e(a), e(b)) for a, b in s["how"]))
    parts.append('<h2>O que você recebe</h2><ul>%s</ul>' % "".join('<li>%s</li>' % e(d) for d in s["deliverables"]))
    parts.append(photo(s["photo"], "%s: registro de campo da AgroAmbient" % s["name"], caption=s["name"]))
    if s["faq"]:
        parts.append('<h2>Perguntas frequentes</h2>' + faq_html(s["faq"]))
    parts.append('<p class="note">Conteúdo informativo. Exigências variam conforme o órgão ambiental, o estado e o tipo de empreendimento.</p>')
    siblings = [x for x in SERVICES if x["area"] == s["area"]]
    aside = """<aside class="aside">
  <div class="aside-card"><h2>Precisa de %s?</h2><p>Conte o tipo de empreendimento e o que o órgão pediu. Respondemos com proposta e prazo.</p>%s<p style="font-size:.9rem">Ou ligue: <a href="tel:%s" data-track="phone_click">%s</a></p></div>
  <div class="aside-card"><h2>%s</h2><ul>%s</ul></div>
</aside>""" % (e(s["name"].lower()), btn(contato_href(assunto), "Pedir orçamento", track="cta_orcamento", local="aside"), SITE["phone_e164"], SITE["phone"],
               e(AREA_NAME[s["area"]]), "".join('<li><a href="/servicos/%s/"%s>%s</a></li>' % (x["slug"], ' aria-current="page"' if x is s else "", e(x["name"])) for x in siblings))
    related = "".join(svc_card(SVC[r]) for r in s["related"] if r in SVC)
    body = hero + """
<section class="sec"><div class="wrap layout">
  <article class="prose">%s</article>
  %s
</div></section>
<section class="sec services"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Serviços relacionados</p><h2>Costumam andar juntos.</h2></div><div class="cards" style="margin-top:2rem">%s</div></div></section>
%s""" % ("\n".join(parts), aside, related, cta_band(assunto=assunto))
    schema = [{"@type": "Service", "@id": abs_url(path) + "#servico", "name": s["name"], "serviceType": s["name"], "description": plain(s["summary"]),
               "url": abs_url(path), "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Country", "name": "Brasil"},
               "category": AREA_NAME[s["area"]]}, crumbs_ld(cr)]
    if s["faq"]:
        schema.append(faq_ld(s["faq"]))
    render(path, s["title"], s["summary"][:300], body, schema=schema)


def page_fauna():
    cr = [("Início", "/"), ("Fauna", "/fauna/")]
    items = [s for s in SERVICES if s["area"] == "fauna"]
    body = hero_page("Estudos de fauna terrestre e aquática.", "Mamíferos, aves, répteis, anfíbios e peixes: levantamento, monitoramento e resgate com especialistas em cada grupo.",
                     cr, eyebrow="Fauna", seed=11, ctas=[btn(contato_href("Estudos de fauna"), "Pedir orçamento", track="cta_orcamento", local="fauna")]) + """
<section class="sec"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Nossa especialidade</p><h2>A fauna é o centro do nosso trabalho.</h2>
<p>Desde o início, a AgroAmbient é especializada em trabalhos com fauna. Planejamos cada estudo para responder ao órgão ambiental com dados de campo confiáveis e identificação correta das espécies.</p></div></div></section>
%s
%s
<section class="sec services"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Serviços de fauna</p><h2>Escolha o estudo que o seu empreendimento precisa.</h2></div>
<div class="cards" style="margin-top:2rem">%s</div></div></section>
%s""" % (fauna_panel(), river_block(link=False), "".join(svc_card(s) for s in items), cta_band(assunto="Estudos de fauna"))
    render("/fauna/", "Estudos de fauna: mastofauna, avifauna, herpetofauna e ictiofauna",
           "Levantamento, monitoramento e resgate de mamíferos, aves, répteis, anfíbios e peixes para licenciamento ambiental, com especialistas em cada grupo.",
           body, schema=[crumbs_ld(cr)])


def page_cursos():
    cr = [("Início", "/"), ("Cursos e palestras", "/cursos-e-palestras/")]
    body = hero_page("Cursos e palestras sobre fauna e meio ambiente.", "Formação para escolas, empresas, cooperativas, produtores rurais e equipes de obra.",
                     cr, eyebrow="Educação ambiental", seed=13, ctas=[btn(contato_href("Cursos e palestras"), "Levar uma palestra", track="cta_palestra", local="hero")]) + """
<section class="sec courses">
  <canvas class="leaves" id="leaves" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Formatos</p><h2>Do bate-papo de uma hora ao programa completo.</h2>
      <p>Adaptamos o conteúdo ao público e ao objetivo: conscientizar, capacitar equipes ou cumprir um programa de educação ambiental exigido na licença.</p></div>
    %s
  </div>
</section>
<section class="sec"><div class="wrap split">
  <div class="prose reveal">
    <h2 style="margin-top:0">Para quem</h2>
    <ul>
      <li>Escolas e universidades.</li>
      <li>Empresas e cooperativas do agro.</li>
      <li>Equipes de obra que atuam em supressão de vegetação e reservatórios.</li>
      <li>Comunidades do entorno de empreendimentos.</li>
      <li>Eventos, feiras e semanas do meio ambiente.</li>
    </ul>
    <p>Quer saber sobre agenda e valores? <a href="/contato/?assunto=Cursos%%20e%%20palestras">Fale com a gente</a>.</p>
  </div>
  <div class="reveal">%s</div>
</div></section>
%s""" % (courses_cards(), photo("cursos", "Curso ministrado pela AgroAmbient", caption="Cursos"), cta_band("Leve a AgroAmbient para a sua instituição.", "Conte o público, a data e o tema que interessa.", "Cursos e palestras"))
    render("/cursos-e-palestras/", "Cursos e palestras de educação ambiental",
           "Palestras e cursos sobre fauna do Cerrado, manejo e resgate de fauna e educação ambiental para escolas, empresas, produtores e equipes de obra.",
           body, schema=[crumbs_ld(cr)])


def page_projetos():
    cr = [("Início", "/"), ("Projetos", "/projetos/")]
    tipos = [("Agropecuária e irrigação", "Licenciamento, outorga e regularização de propriedades e projetos de irrigação."),
             ("Barragens e reservatórios", "Ictiofauna, resgate de peixes, transposição e monitoramento."),
             ("Obras lineares", "Estradas, linhas de transmissão e dutos com afugentamento e resgate de fauna."),
             ("Mineração", "Diagnóstico, inventário e monitoramento de fauna e PRAD."),
             ("Loteamentos e indústrias", "Estudos ambientais para licença e condicionantes."),
             ("Áreas protegidas", "Planos de manejo e programas de conservação.")]
    cards = "".join('<article class="card reveal" style="--d:%.2fs"><p class="eyebrow">Empreendimento</p><h3>%s</h3><p>%s</p></article>' % ((i % 3) * .06, e(a), e(b)) for i, (a, b) in enumerate(tipos))
    setores = "".join('<li>%s</li>' % e(x) for x in SECTORS)
    body = hero_page("Projetos e tipos de empreendimento.", "Estudos ambientais para empreendimentos rurais, de infraestrutura, energia e mineração.",
                     cr, eyebrow="Projetos", seed=17) + """
<section class="sec"><div class="wrap stack-lg">
  <div><div class="sec-head reveal"><p class="eyebrow">Para quem trabalhamos</p><h2>Empreendimentos que costumam precisar de estudos de fauna.</h2></div><div class="cards" style="margin-top:2rem">%s</div></div>
  <div><div class="sec-head reveal"><p class="eyebrow">Setores atendidos</p><h2>Mineração, energia, agro, indústria e consultorias.</h2><p>Atendemos diretamente os empreendimentos e também empresas de consultoria e gestão ambiental que precisam de equipe especializada em fauna.</p></div><ul class="checks reveal">%s</ul></div>
  <div><div class="sec-head reveal"><p class="eyebrow">Do campo</p><h2>Registros dos nossos trabalhos.</h2></div><div style="margin-top:2rem">%s</div></div>
  <div><div class="sec-head reveal"><p class="eyebrow">Clientes e parceiros</p><h2>Quem confia no nosso trabalho.</h2></div>
  %s
  <p class="reveal" style="margin-top:1.6rem">%s</p></div>
</div></section>
%s""" % (cards, setores, gallery(), partners_html(), portfolio_btn("projetos", "btn-ipe"), cta_band())
    render("/projetos/", "Projetos e tipos de empreendimento atendidos",
           "Estudos de fauna e assessoria ambiental para mineração, energia, agropecuária, indústria e consultorias. Clientes como Mosaic Fertilizantes, RHI Magnesita e EuroChem.",
           body, schema=[crumbs_ld(cr)])


def page_faq():
    cr = [("Início", "/"), ("Perguntas frequentes", "/perguntas-frequentes/")]
    groups = "".join('<div class="faq-group reveal"><h2>%s</h2>%s</div>' % (e(g), faq_html(pairs)) for g, pairs in FAQ)
    allpairs = [p for _, pairs in FAQ for p in pairs]
    body = hero_page("Perguntas frequentes sobre estudos ambientais.", "Fauna, licenciamento, outorga, prazos e orçamento, em respostas diretas.", cr,
                     eyebrow="Perguntas frequentes", seed=19) + """
<section class="sec"><div class="wrap">%s</div></section>
%s""" % (groups, cta_band("Não encontrou sua dúvida?", "Pergunte direto para a nossa equipe."))
    render("/perguntas-frequentes/", "Perguntas frequentes sobre estudos de fauna e licenciamento",
           "Respostas sobre inventário e monitoramento de fauna, resgate, licenciamento ambiental, outorga de água, prazos e orçamento.",
           body, schema=[faq_ld(allpairs), crumbs_ld(cr)])


def page_blog():
    cr = [("Início", "/"), ("Blog", "/blog/")]
    body = hero_page("Blog da AgroAmbient.", "Guias práticos sobre fauna, licenciamento ambiental e regularização rural.", cr, eyebrow="Blog", seed=23) + """
<section class="sec"><div class="wrap"><div class="cards">%s</div></div></section>
%s""" % ("".join(post_card(p) for p in POSTS), cta_band())
    render("/blog/", "Blog: fauna, licenciamento e regularização ambiental",
           "Artigos e guias da AgroAmbient sobre estudos de fauna, resgate, licenciamento ambiental e outorga de água em Minas Gerais.",
           body, schema=[{"@type": "Blog", "url": abs_url("/blog/"), "name": "Blog da AgroAmbient", "publisher": {"@id": ORG_ID},
                          "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": abs_url("/blog/%s/" % p["slug"])} for p in POSTS]}, crumbs_ld(cr)])


def render_post_body(blocks):
    out = []
    for kind, val in blocks:
        if kind == "h2":
            slug = re.sub(r"[^a-z0-9]+", "-", val.lower().encode("ascii", "ignore").decode()).strip("-")
            out.append('<h2 id="%s">%s</h2>' % (slug, e(val)))
        elif kind == "p":
            out.append("<p>%s</p>" % val)
        elif kind in ("ul", "ol"):
            out.append("<%s>%s</%s>" % (kind, "".join("<li>%s</li>" % x for x in val), kind))
        elif kind == "table":
            head, rows = val[0], val[1:]
            out.append('<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
                "".join("<th>%s</th>" % e(h) for h in head), "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % e(c) for c in r) for r in rows)))
    return "\n".join(out)


def page_post(p):
    path = "/blog/%s/" % p["slug"]
    cr = [("Início", "/"), ("Blog", "/blog/"), (p["title"], path)]
    d = datetime.date.fromisoformat(p["date"])
    words = len(plain(" ".join(str(v) for _, v in p["body"])).split())
    meta = '<p class="post-meta"><time datetime="%s">%s</time> · %d min de leitura · Equipe AgroAmbient</p>' % (p["date"], d.strftime("%d/%m/%Y"), max(1, round(words / 200)))
    hero = hero_page(p["title"], p["description"], cr, eyebrow="Blog", seed=29 + POSTS.index(p), meta=meta)
    toc = "".join('<li><a href="#%s">%s</a></li>' % (re.sub(r"[^a-z0-9]+", "-", v.lower().encode("ascii", "ignore").decode()).strip("-"), e(v)) for k, v in p["body"] if k == "h2")
    aside = """<aside class="aside">
  <div class="aside-card toc"><h2>Neste artigo</h2><ul>%s</ul></div>
  <div class="aside-card"><h2>Serviços relacionados</h2><ul>%s</ul>%s</div>
</aside>""" % (toc, "".join('<li><a href="/servicos/%s/">%s</a></li>' % (r, e(SVC[r]["name"])) for r in p["related"]), btn("/contato/", "Pedir orçamento", track="cta_orcamento", local="blog"))
    body = '<div id="readBar" aria-hidden="true"></div>' + hero + """
<section class="sec"><div class="wrap layout">
  <article class="prose">
    <div class="summary"><span class="label">Resposta curta</span><p>%s</p></div>
    %s
    <p class="note">Conteúdo informativo, atualizado em %s. As exigências variam conforme o órgão ambiental e o tipo de empreendimento.</p>
  </article>
  %s
</div></section>
<section class="sec services"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Continue lendo</p><h2>Outros artigos.</h2></div><div class="cards" style="margin-top:2rem">%s</div></div></section>
%s""" % (e(p["summary"]), render_post_body(p["body"]), d.strftime("%d/%m/%Y"), aside, "".join(post_card(x) for x in POSTS if x is not p), cta_band())
    schema = [{"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "datePublished": p["date"], "dateModified": p["date"],
               "inLanguage": "pt-BR", "mainEntityOfPage": abs_url(path), "url": abs_url(path), "image": abs_url("/static/og.png"),
               "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "abstract": p["summary"]}, crumbs_ld(cr)]
    render(path, p["title"], p["description"], body, schema=schema, og_type="article")


def page_contato():
    cr = [("Início", "/"), ("Contato", "/contato/")]
    body = hero_page("Fale com a AgroAmbient.", "Peça um orçamento, tire dúvidas sobre o licenciamento ou agende uma palestra.", cr, eyebrow="Contato", seed=31) + """
<section class="sec"><div class="wrap">%s</div></section>""" % contact_block()
    render("/contato/", "Contato e orçamento",
           "Solicite orçamento de estudos de fauna, licenciamento ambiental e outorga. WhatsApp (34) 99806-7566 e telefone (34) 3855-1197. Sede em Catalão (GO).",
           body, schema=[{"@type": "ContactPage", "url": abs_url("/contato/"), "name": "Contato AgroAmbient", "about": {"@id": ORG_ID}}, crumbs_ld(cr)])


def page_privacidade():
    cr = [("Início", "/"), ("Política de privacidade", "/politica-de-privacidade/")]
    body = hero_page("Política de privacidade.", "Como a AgroAmbient trata os dados de quem visita o site e entra em contato.", cr, eyebrow="LGPD", seed=37) + """
<section class="sec"><div class="wrap"><article class="prose">
<p>Esta política explica como a %s (“AgroAmbient”), CNPJ %s, com sede em %s, %s/%s, trata dados pessoais neste site, conforme a Lei Geral de Proteção de Dados (Lei nº 13.709/2018).</p>
<h2>Quais dados coletamos</h2>
<ul>
<li><strong>Dados que você envia:</strong> nome, cidade, assunto e mensagem, quando você usa o formulário de contato. O formulário não guarda nada no site: ele abre o WhatsApp com a mensagem pronta, e a conversa segue pelo WhatsApp, sujeita também à política do aplicativo.</li>
<li><strong>Dados de navegação:</strong> páginas visitadas, tipo de dispositivo e origem da visita, coletados por cookies do Google Analytics e do Google Ads, somente se você aceitar no aviso de cookies.</li>
</ul>
<h2>Para que usamos</h2>
<ul>
<li>Responder pedidos de orçamento e dúvidas.</li>
<li>Entender como o site é usado e melhorar o conteúdo.</li>
<li>Medir o resultado de anúncios.</li>
</ul>
<h2>Base legal</h2>
<p>Usamos os dados de contato para atender ao seu pedido e para procedimentos preliminares de contrato. Os cookies de medição e publicidade dependem do seu consentimento, que pode ser retirado a qualquer momento em “Preferências de cookies”, no rodapé.</p>
<h2>Compartilhamento</h2>
<p>Não vendemos dados pessoais. Os dados de navegação são processados pelo Google (Analytics e Ads) quando você consente. Podemos compartilhar dados quando exigido por lei ou por autoridade competente.</p>
<h2>Por quanto tempo guardamos</h2>
<p>Pelo tempo necessário para atender ao pedido e cumprir obrigações legais.</p>
<h2>Seus direitos</h2>
<p>Você pode pedir confirmação, acesso, correção, anonimização, portabilidade ou exclusão dos seus dados, e informações sobre compartilhamento, conforme o artigo 18 da LGPD. Escreva para <strong>%s</strong>.</p>
<p class="note">Última atualização: %s.</p>
</article></div></section>""" % (SITE["legal_name"], SITE["cnpj"], SITE["street"], SITE["city"], SITE["region"], SITE["email"], datetime.date.today().strftime("%d/%m/%Y"))
    render("/politica-de-privacidade/", "Política de privacidade", "Como a AgroAmbient trata dados pessoais e cookies neste site, conforme a LGPD.", body, schema=[crumbs_ld(cr)])


def page_404():
    body = hero_page("Página não encontrada.", "O endereço pode ter mudado com o novo site. Veja os caminhos mais procurados abaixo.", [("Início", "/"), ("Página não encontrada", "/404")],
                     seed=41, ctas=[btn("/", "Ir para o início"), '<a class="btn btn-ghost" href="/servicos/">Ver serviços</a>', '<a class="btn btn-ghost" href="/contato/">Contato</a>'])
    render("/404", "Página não encontrada", "A página procurada não existe.", body, noindex=True)


# ---------------------------------------------------------------------------
# arquivos de SEO e IA
# ---------------------------------------------------------------------------
def write_seo_files():
    prio = lambda p: "1.0" if p == "/" else ("0.9" if p.startswith("/servicos/") else "0.7")
    urls = "".join("<url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (abs_url(p), TODAY, prio(p)) for p, _, _ in PAGES)
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls, encoding="utf-8")

    bots = ["Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "DuckAssistBot", "Meta-ExternalAgent", "CCBot"]
    robots = "# Site aberto para buscadores e assistentes de IA.\n" + "".join("User-agent: %s\nAllow: /\n\n" % b for b in bots) + \
             "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % U
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")

    # llms.txt: resumo navegável para assistentes de IA (formato llmstxt.org)
    L = ["# AgroAmbient", "", "> %s" % SITE["description"], "",
         "- Empresa: %s" % SITE["legal_name"],
         "- Sede: %s, %s, %s/%s, Brasil" % (SITE["street"], SITE["city"], SITE["region"], SITE["postal"]),
         "- Atuação: todo o território nacional, com base em Catalão (GO), na divisa com Minas Gerais",
         "- Telefone: %s" % SITE["phone"], "- WhatsApp: %s" % SITE["whatsapp"], "- E-mail: %s" % SITE["email"],
         "- Fundação: %s" % SITE["founded"], "- CNPJ: %s" % SITE["cnpj"], "- CTF/IBAMA: %s" % SITE["ctf"], "- Registro CRBio-04: %s" % SITE["crbio"],
         "- Direção técnica: %s, %s" % (SITE["founder"], SITE["founder_title"]),
         "- Setores atendidos: %s" % ", ".join(SECTORS),
         "- Clientes e parceiros: %s" % ", ".join(PARTNERS),
         "- Portfólio em PDF: %s%s" % (U, SITE["portfolio_pdf"]),
         "- Especialidade: estudos de fauna terrestre e aquática (mastofauna, avifauna, herpetofauna, ictiofauna)",
         "- Missão: oferecer produtos, soluções e a execução de trabalhos de qualidade aos clientes, aliando produtividade, eficiência e preservação do meio ambiente.", "",
         "## Serviços", ""]
    L += ["- [%s](%s/servicos/%s/): %s" % (s["name"], U, s["slug"], plain(s["short"])) for s in SERVICES]
    L += ["- [Cursos e palestras](%s/cursos-e-palestras/): palestras, cursos e programas de educação ambiental." % U, "",
          "## Páginas principais", "",
          "- [Sobre](%s/sobre/): história, missão, visão e equipe." % U,
          "- [Fauna](%s/fauna/): grupos de fauna estudados e métodos." % U,
          "- [Perguntas frequentes](%s/perguntas-frequentes/): respostas sobre fauna, licenciamento, prazos e orçamento." % U,
          "- [Contato](%s/contato/): orçamento e dados de contato." % U, "", "## Artigos", ""]
    L += ["- [%s](%s/blog/%s/): %s" % (p["title"], U, p["slug"], p["description"]) for p in POSTS]
    L += ["", "## Opcional", "", "- [Texto completo do site](%s/llms-full.txt): todo o conteúdo em texto simples." % U, ""]
    (DIST / "llms.txt").write_text("\n".join(L), encoding="utf-8")

    F = ["# AgroAmbient: conteúdo completo", "", SITE["description"], ""]
    for s in SERVICES:
        F += ["## %s" % s["title"], "URL: %s/servicos/%s/" % (U, s["slug"]), "", plain(s["summary"]), ""] + [plain(x) for x in s["intro"]] + [""]
        F += ["Quando é necessário:"] + ["- " + plain(w) for w in s["when"] if plain(w)] + [""]
        F += ["Como fazemos:"] + ["%d. %s: %s" % (i + 1, a, b) for i, (a, b) in enumerate(s["how"])] + [""]
        for q, a in s["faq"]:
            F += ["P: " + q, "R: " + plain(a), ""]
    F += ["## Perguntas frequentes", ""]
    for g, pairs in FAQ:
        F += ["### " + g, ""]
        for q, a in pairs:
            F += ["P: " + q, "R: " + plain(a), ""]
    for p in POSTS:
        F += ["## " + p["title"], "URL: %s/blog/%s/" % (U, p["slug"]), "", p["summary"], ""]
        for k, v in p["body"]:
            if k == "h2":
                F += ["### " + v]
            elif k == "p":
                F += [plain(v), ""]
            elif k in ("ul", "ol"):
                F += ["- " + plain(x) for x in v] + [""]
            elif k == "table":
                F += [" | ".join(r) for r in v] + [""]
    (DIST / "llms-full.txt").write_text("\n".join(F), encoding="utf-8")

    manifest = {"name": SITE["legal_name"], "short_name": "AgroAmbient", "lang": "pt-BR", "start_url": "/", "display": "standalone",
                "background_color": "#F1F3EA", "theme_color": "#13201A",
                "icons": [{"src": "/static/icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "/static/icon-512.png", "sizes": "512x512", "type": "image/png"},
                          {"src": "/static/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}
    (DIST / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------------------------------------------------------------------------
def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets").mkdir(parents=True)
    for f in ("site.css", "site.js"):
        shutil.copy(ROOT / "assets" / f, DIST / "assets" / f)
    ASSET_V["css"] = file_hash(ROOT / "assets" / "site.css")
    ASSET_V["js"] = file_hash(ROOT / "assets" / "site.js")
    if (ROOT / "static").exists():
        shutil.copytree(ROOT / "static", DIST / "static")
    page_home()
    page_sobre()
    page_servicos()
    for s in SERVICES:
        page_service(s)
    page_fauna()
    page_cursos()
    page_projetos()
    page_faq()
    page_blog()
    for p in POSTS:
        page_post(p)
    page_contato()
    page_privacidade()
    page_404()
    write_seo_files()
    print("Site gerado em dist/ com %d páginas indexáveis." % len(PAGES))


if __name__ == "__main__":
    main()
