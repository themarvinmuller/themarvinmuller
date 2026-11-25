import { getConfig, getBallots } from '../../lib/store.js';
import { json, isAdmin } from '../../lib/http.js';
import { tally } from '../../lib/tally.js';

// Painel: configuração, quem já votou e (opcional) resultado.
export async function GET(request) {
  if (!isAdmin(request)) return json({ error: 'Senha incorreta.' }, 401);
  const cfg = await getConfig({ fresh: true });
  const ballots = await getBallots();
  const withResults = new URL(request.url).searchParams.get('results') === '1';
  return json({
    config: cfg,
    voters: ballots
      .map((b) => ({ name: b.voter, categories: Object.keys(b.votes || {}).length, savedAt: b.savedAt }))
      .sort((a, b) => a.name.localeCompare(b.name, 'pt-BR')),
    results: withResults ? tally(ballots, cfg.participants) : undefined,
  });
}
