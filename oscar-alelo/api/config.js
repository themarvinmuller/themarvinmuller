import { getConfig } from '../lib/store.js';
import { json } from '../lib/http.js';

// Dados públicos para a página de votação.
export async function GET() {
  const cfg = await getConfig();
  return json(
    {
      eventName: cfg.eventName,
      participants: cfg.participants,
      votingOpen: cfg.votingOpen,
      allowSelfVote: cfg.allowSelfVote,
      needsCode: Boolean(cfg.accessCode),
    },
    200,
    { 'cache-control': 'public, s-maxage=15, stale-while-revalidate=30' },
  );
}
