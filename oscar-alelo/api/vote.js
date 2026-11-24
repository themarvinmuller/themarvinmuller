import { CATEGORIES } from '../public/assets/categories.js';
import { getConfig, saveBallot, normalize } from '../lib/store.js';
import { json, readBody } from '../lib/http.js';

export async function POST(request) {
  const body = await readBody(request);
  if (!body) return json({ error: 'Pedido inválido.' }, 400);
  const cfg = await getConfig({ fresh: true });
  if (!cfg.votingOpen) return json({ error: 'A votação está encerrada.' }, 403);
  if (cfg.accessCode && normalize(body.code) !== normalize(cfg.accessCode)) {
    return json({ error: 'Código de acesso incorreto.' }, 403);
  }

  const official = new Map(cfg.participants.map((p) => [normalize(p), p]));
  const voter = official.get(normalize(body.voter));
  if (!voter) return json({ error: 'Escolha seu nome na lista.' }, 400);

  const votes = {};
  for (const cat of CATEGORIES) {
    const raw = body.votes?.[cat.id];
    if (!raw) continue;
    const name = official.get(normalize(raw));
    if (!name) return json({ error: `Nome inválido em "${cat.name}".` }, 400);
    if (!cfg.allowSelfVote && normalize(name) === normalize(voter)) {
      return json({ error: `Não vale votar em si mesmo(a) em "${cat.name}".` }, 400);
    }
    const dup = Object.entries(votes).find(([, v]) => v === name);
    if (dup) {
      const other = CATEGORIES.find((c) => c.id === dup[0]).name;
      return json({ error: `${name} já foi escolhido(a) em "${other}". Cada pessoa só pode ser escolhida uma vez.` }, 400);
    }
    votes[cat.id] = name;
  }
  if (!Object.keys(votes).length) return json({ error: 'Escolha pelo menos uma categoria.' }, 400);

  await saveBallot({ voter, votes });
  return json({ ok: true, voter, count: Object.keys(votes).length });
}
