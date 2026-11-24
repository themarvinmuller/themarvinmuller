import { getConfig, saveConfig, normalize } from '../../lib/store.js';
import { json, isAdmin, readBody } from '../../lib/http.js';

export async function POST(request) {
  if (!isAdmin(request)) return json({ error: 'Senha incorreta.' }, 401);
  const body = await readBody(request);
  if (!body) return json({ error: 'Pedido inválido.' }, 400);
  const cur = await getConfig({ fresh: true });
  const next = { ...cur };
  if (typeof body.eventName === 'string') next.eventName = body.eventName.trim().slice(0, 80) || cur.eventName;
  if (Array.isArray(body.participants)) {
    const seen = new Set();
    next.participants = body.participants
      .map((p) => String(p).trim().replace(/\s+/g, ' ').slice(0, 80))
      .filter((p) => p && !seen.has(normalize(p)) && seen.add(normalize(p)))
      .sort((a, b) => a.localeCompare(b, 'pt-BR'));
  }
  if (typeof body.votingOpen === 'boolean') next.votingOpen = body.votingOpen;
  if (typeof body.allowSelfVote === 'boolean') next.allowSelfVote = body.allowSelfVote;
  if (typeof body.accessCode === 'string') next.accessCode = body.accessCode.trim().slice(0, 40);
  const saved = await saveConfig(next);
  return json({ ok: true, config: saved });
}
