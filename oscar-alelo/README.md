# Oscar de fim de ano

Site de votação estilo Oscar ("Oscar CRM 2026") para a festa de fim de ano. Cada pessoa escolhe seu nome numa lista e indica **uma pessoa por categoria** (24 categorias). Na festa, a página de cerimônia revela os vencedores um a um.

Publicado na Vercel (projeto `oscar-alelo`, Root Directory `oscar-alelo`). Os votos ficam num store privado do Vercel Blob.

## Páginas

| Página | Para quem |
| --- | --- |
| `/` | Votação (mandar este link para o pessoal) |
| `/admin` | Organização: participantes, abrir/fechar votação, quem já votou, resultado, CSV |
| `/cerimonia` | Telão: indicados, envelope e vencedor com confete, categoria por categoria |

`/admin` e `/cerimonia` pedem a senha definida na variável `ADMIN_PASSWORD` da Vercel.

## Regras

- Lista suspensa com os nomes cadastrados no painel (sem texto livre).
- Uma pessoa por categoria, e cada pessoa só pode ser escolhida em uma categoria (as já escolhidas ficam desabilitadas nas outras listas). Dá para pular categorias.
- Não dá para votar em si mesmo(a) (pode ser liberado no painel).
- Votar de novo com o mesmo nome substitui o voto anterior.
- Código da festa opcional para evitar votos de fora.
- Indicados na cerimônia = os 3 mais votados (empates em 1º aparecem juntos).

## Onde mudar

| O que | Onde |
| --- | --- |
| Categorias, ícones e descrições | `public/assets/categories.js` |
| Visual | `public/assets/style.css` |
| Regras de voto | `api/vote.js` |
| Contagem | `lib/tally.js` |

## Rodar local

```bash
npm install
npm run dev     # http://localhost:3000 — senha local do painel: admin
```

Sem `BLOB_READ_WRITE_TOKEN`, os dados ficam em `.data/`.
