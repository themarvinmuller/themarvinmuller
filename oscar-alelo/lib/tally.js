import { CATEGORIES } from '../public/assets/categories.js';
import { normalize } from './store.js';

// Conta os votos por categoria. Nomes iguais com acento/maiúscula diferentes
// são somados juntos; o nome exibido é o mais usado (ou o da lista oficial).
export function tally(ballots, participants = []) {
  const official = new Map(participants.map((p) => [normalize(p), p]));
  return CATEGORIES.map((cat) => {
    const counts = new Map();
    for (const b of ballots) {
      const name = b.votes?.[cat.id];
      if (!name || !String(name).trim()) continue;
      const k = normalize(name);
      if (!counts.has(k)) counts.set(k, { votes: 0, spellings: new Map() });
      const c = counts.get(k);
      c.votes += 1;
      const s = String(name).trim();
      c.spellings.set(s, (c.spellings.get(s) || 0) + 1);
    }
    const ranking = [...counts.entries()]
      .map(([k, c]) => ({
        name: official.get(k) || [...c.spellings.entries()].sort((a, b) => b[1] - a[1])[0][0],
        votes: c.votes,
      }))
      .sort((a, b) => b.votes - a.votes || a.name.localeCompare(b.name, 'pt-BR'));
    const top = ranking[0]?.votes || 0;
    return {
      id: cat.id,
      name: cat.name,
      icon: cat.icon,
      totalVotes: ranking.reduce((s, r) => s + r.votes, 0),
      winners: top ? ranking.filter((r) => r.votes === top).map((r) => r.name) : [],
      ranking,
    };
  });
}
