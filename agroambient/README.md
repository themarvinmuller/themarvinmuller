# Site AgroAmbient (primeira versão)

Novo site institucional da AgroAmbient para o domínio `.com.br`. Página única, sem dependências de build.

- `src/site.html`: fonte (conteúdo, estilos e scripts).
- `build.py`: gera `index.html` com `<head>` completo (SEO, Open Graph, dados estruturados LocalBusiness).
- `index.html`: arquivo pronto para hospedar.

```bash
python3 build.py   # regenera index.html depois de editar src/site.html
```

## Efeitos
- Herói do Cerrado ao entardecer, gerado em SVG (chapadas, buritis, capim) com parallax no scroll e no mouse, vagalumes e revoada de aves em canvas.
- Seção "rio" com peixes que fogem do cursor, raios de luz e bolhas.
- Painel horizontal dos grupos de fauna preso ao scroll (vira carrossel no celular).
- Trilha do processo que se desenha conforme o scroll, folhas caindo em Cursos e palestras.
- Respeita `prefers-reduced-motion` e tem tema claro e escuro.

## Pendências (marcadas no site como "a confirmar")
- Celular/WhatsApp completo (o site atual mostra um dígito a menos) e link do botão flutuante.
- @ do Instagram, ano de fundação, cargo e registro de Willian Lopes Silva.
- Se piscicultura e sistemas agroflorestais continuam sendo oferecidos.
- CNPJ, CTF/IBAMA, logos de clientes autorizados, temas reais de cursos.
- Conectar o formulário a um serviço de envio.
- Fotos: hoje apontam para o Wix atual (`static.wixstatic.com`). Baixar em boa resolução e hospedar junto com o site antes de desligar o Wix.
- Redirecionamentos 301 de agroambient.net para o novo domínio.
