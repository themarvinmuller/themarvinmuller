#!/usr/bin/env python3
"""Gera index.html (documento completo para hospedagem) a partir de src/site.html."""
import json, pathlib
here = pathlib.Path(__file__).parent
body = (here / "src" / "site.html").read_text(encoding="utf-8")
# remove a meta usada só na prévia
body = body.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
title, rest = body.split("\n", 1)
ld = {
  "@context": "https://schema.org", "@type": "ProfessionalService",
  "name": "AgroAmbient Assessoria Agroambiental",
  "description": "Consultoria ambiental especializada em estudos de fauna terrestre e aquática, licenciamento e assessoria agroambiental.",
  "url": "https://www.agroambient.com.br/",
  "telephone": "+55 34 3855-1197", "email": "agroambient@gmail.com",
  "address": {"@type": "PostalAddress", "streetAddress": "Rua Joaquim Lopes da Silva, 291",
              "addressLocality": "Rio Paranaíba", "addressRegion": "MG", "postalCode": "38810-000", "addressCountry": "BR"},
  "areaServed": "BR", "sameAs": ["https://www.facebook.com/AgroAmbient"]
}
head = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>AgroAmbient | Consultoria ambiental e estudos de fauna em Minas Gerais</title>
<meta name="description" content="Estudos de fauna terrestre e aquática, licenciamento ambiental, outorga e assessoria agroambiental em todo o Brasil, a partir do Alto Paranaíba (MG).">
<link rel="canonical" href="https://www.agroambient.com.br/">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="AgroAmbient | Preservação ambiental, plante esta ideia.">
<meta property="og:description" content="Consultoria ambiental especializada em fauna terrestre e aquática.">
<meta name="theme-color" content="#13201A">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>:root{{padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>
"""
out = head + rest.replace("</style>\n", "</style>\n</head>\n<body>\n", 1) + "\n</body>\n</html>\n"
(here / "index.html").write_text(out, encoding="utf-8")
print("index.html gerado")
