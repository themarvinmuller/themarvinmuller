# Site AgroAmbient

Site institucional da AgroAmbient (consultoria ambiental especializada em fauna). Estático, gerado por um script Python sem dependências e publicado na Vercel (projeto `agroambient-site`, Root Directory `agroambient`).

## Como editar

| O que mudar | Onde |
| --- | --- |
| Textos, serviços, FAQ, artigos, contatos, IDs do GA4/Ads | `content.py` |
| Layout das páginas e dados estruturados | `build.py` |
| Estilos | `assets/site.css` |
| Efeitos e interações | `assets/site.js` |
| Favicon, ícones e imagem de compartilhamento | `static/` |
| Redirecionamentos, cabeçalhos e build da Vercel | `vercel.json` |

```bash
python3 build.py                        # gera dist/
python3 -m http.server 8000 -d dist     # abre em http://localhost:8000
```

A Vercel roda `python3 build.py` a cada push e publica `dist/` (configurado em `vercel.json`).

## Páginas (25 indexáveis)
Início, Sobre, Serviços, 12 páginas de serviço, Fauna, Cursos e palestras, Projetos, Perguntas frequentes, Blog com 3 artigos, Contato, Política de privacidade e 404.

## SEO
- Título, descrição, canonical, Open Graph e Twitter Card por página.
- Dados estruturados (JSON-LD): Organization + ProfessionalService com endereço, geo, área atendida e catálogo de serviços; WebSite; BreadcrumbList; Service; FAQPage; Blog/BlogPosting; AboutPage; ContactPage.
- `sitemap.xml`, `robots.txt`, `manifest.webmanifest`, 404 própria.
- Redirecionamentos 301 dos endereços do site antigo (`/a-empresa`, `/assessoria-ambiental`, `/portfolio`, `/fale-conocsco`).
- Quando o domínio .com.br estiver na Vercel: trocar `SITE["url"]` em `content.py`, adicionar o domínio no projeto e cadastrar o sitemap no Google Search Console.

## Visibilidade para IA
- `llms.txt` (resumo navegável, formato llmstxt.org) e `llms-full.txt` (conteúdo completo em texto).
- `robots.txt` libera explicitamente buscadores e assistentes (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended e outros).
- Cada serviço e artigo abre com uma resposta curta ("Em resumo" / "Resposta curta"), em HTML semântico.

## Medição (GA4 e Google Ads)
Preencha em `content.py`:

```python
"ga4": "G-XXXXXXX", "ads": "AW-XXXXXXXXX", "ads_lead_label": "rotulo",
```

- Com IDs vazios, nenhum script do Google é carregado e o aviso de cookies não aparece.
- Consent Mode v2 com aviso de cookies (LGPD): tudo começa negado e só libera com "Aceitar". Link "Preferências de cookies" no rodapé.
- Eventos: `generate_lead` (formulário, com o assunto), `whatsapp_click`, `phone_click`, `cta_orcamento`, `cta_palestra`, `copy_phone`, `copy_email`, `faq_open`, `download_portfolio`. Todos vão também para o `dataLayer` (serve ao Google Tag Manager).
- Conversão do Ads: com `ads` e `ads_lead_label`, o envio do formulário dispara a conversão de lead. No GA4, marque `generate_lead` como evento-chave.

## Formulário
Formulário curto (nome, cidade, assunto, mensagem opcional). Ao enviar, abre o WhatsApp da empresa com a mensagem pronta e dispara o evento `generate_lead` (e a conversão do Ads). O número vem de `whatsapp_e164` em `content.py` (só dígitos, com 55 e DDD). Enquanto estiver vazio, o envio cai no e-mail `agroambient@gmail.com`.

## Pendências (marcadas no site como "a confirmar")
- WhatsApp completo (`whatsapp_e164`), @ do Instagram, ano de fundação, CNPJ, CTF/IBAMA.
- Cargo, formação e registro de Willian Lopes Silva e da equipe.
- Se piscicultura e sistemas agroflorestais continuam sendo oferecidos.
- Logos de clientes autorizados, cases de projetos, agenda real de cursos.
- Fotos: hoje vêm do Wix antigo (`static.wixstatic.com`). Baixar em boa resolução para `static/` antes de desligar o Wix.
