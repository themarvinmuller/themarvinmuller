import { deleteAllVotes } from '../../lib/store.js';
import { json, isAdmin, readBody } from '../../lib/http.js';

export async function POST(request) {
  if (!isAdmin(request)) return json({ error: 'Senha incorreta.' }, 401);
  const body = await readBody(request);
  if (body?.confirm !== 'APAGAR') return json({ error: 'Confirmação ausente.' }, 400);
  const removed = await deleteAllVotes();
  return json({ ok: true, removed });
}
