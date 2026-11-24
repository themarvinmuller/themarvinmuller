// Armazenamento dos dados do Oscar.
// Em produção usa o Vercel Blob (store privado). Sem BLOB_READ_WRITE_TOKEN,
// grava em ./.data (para rodar local com `npm run dev`).
//
// Cada gravação cria um arquivo novo e imutável (sufixo aleatório). A versão
// válida de cada chave é a mais recente; assim não existe problema de cache
// nem de duas pessoas gravando o mesmo arquivo ao mesmo tempo.
import { promises as fs } from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const USE_BLOB = Boolean(process.env.BLOB_READ_WRITE_TOKEN);
const ROOT = 'oscar/';
const LOCAL_DIR = path.join(process.cwd(), '.data');

let blobMod;
async function blob() {
  if (!blobMod) blobMod = await import('@vercel/blob');
  return blobMod;
}

// Lista { pathname, uploadedAt(ms), ref } com o prefixo dado.
async function listItems(prefix) {
  const full = ROOT + prefix;
  if (USE_BLOB) {
    const { list } = await blob();
    const out = [];
    let cursor;
    do {
      const r = await list({ prefix: full, cursor, limit: 1000 });
      for (const b of r.blobs) {
        out.push({ pathname: b.pathname.slice(ROOT.length), uploadedAt: new Date(b.uploadedAt).getTime(), ref: b.url });
      }
      cursor = r.hasMore ? r.cursor : undefined;
    } while (cursor);
    return out;
  }
  await fs.mkdir(LOCAL_DIR, { recursive: true });
  const files = await fs.readdir(LOCAL_DIR);
  const out = [];
  for (const f of files) {
    const p = decodeURIComponent(f);
    if (!p.startsWith(full)) continue;
    const st = await fs.stat(path.join(LOCAL_DIR, f));
    out.push({ pathname: p.slice(ROOT.length), uploadedAt: st.mtimeMs, ref: path.join(LOCAL_DIR, f) });
  }
  return out;
}

async function readItem(item) {
  if (USE_BLOB) {
    const { get } = await blob();
    const r = await get(item.ref, { access: 'private' });
    if (!r || r.statusCode !== 200) return null;
    return JSON.parse(await new Response(r.stream).text());
  }
  return JSON.parse(await fs.readFile(item.ref, 'utf8'));
}

async function writeJson(pathname, data) {
  const body = JSON.stringify(data);
  if (USE_BLOB) {
    const { put } = await blob();
    await put(ROOT + pathname, body, {
      access: 'private',
      addRandomSuffix: true,
      contentType: 'application/json',
    });
    return;
  }
  await fs.mkdir(LOCAL_DIR, { recursive: true });
  const name = ROOT + pathname.replace(/\.json$/, '') + '-' + crypto.randomBytes(6).toString('hex') + '.json';
  await fs.writeFile(path.join(LOCAL_DIR, encodeURIComponent(name)), body);
}

async function deleteItems(items) {
  if (!items.length) return;
  if (USE_BLOB) {
    const { del } = await blob();
    for (let i = 0; i < items.length; i += 500) {
      await del(items.slice(i, i + 500).map((x) => x.ref));
    }
    return;
  }
  await Promise.all(items.map((x) => fs.unlink(x.ref).catch(() => {})));
}

// Agrupa por chave (pasta + id antes do sufixo) e fica com o mais recente.
function latestByKey(items) {
  const map = new Map();
  for (const it of items) {
    const key = it.pathname.split('/').slice(0, 2).join('/');
    const cur = map.get(key);
    if (!cur || it.uploadedAt > cur.uploadedAt) map.set(key, it);
  }
  return map;
}

// ---------- Configuração ----------
export const DEFAULT_CONFIG = {
  eventName: 'Oscar Alelo 2026',
  // Lista inicial; pode ser editada no painel (/admin).
  participants: ["Ana Gabriela de Carvalho", "André Phillipe Mansano", "Aryel da Silva Sampaio", "Bianca Ribeiro Melo", "Cristiane Justino dos Santos", "Eduardo Souza Borges", "Elizabeth dos Santos", "Frederico Augusto Tomaz Monteiro", "Fulvio", "Gabriel Vieira Barbosa", "Gladson Barreto", "Janice dos Santos Almeida", "Joao Pedro Costa Lima", "José Lourenço da Silva Neto", "Karina Moimas", "Leticia Oliveira Nascimento", "Luciano Mateus Almeida Cardoso", "Ludmila dos Santos Silva", "Luísa Menezes de Mattos", "Matheus Alarcon Brunchner", "Michel Allan Goncalves Romera", "Nathalia Barreto Alegretti", "Patrícia Regina Corrêa", "Rafael Alcantara de Freitas", "Tatiana", "Viviane Oliani Andrade", "Waldinei Comercio de Souza Guimarães", "Willian Alves Rosa"],
  votingOpen: true,
  allowSelfVote: false,
  accessCode: '',
};

let configCache = { at: 0, value: null };

export async function getConfig({ fresh = false } = {}) {
  if (!fresh && configCache.value && Date.now() - configCache.at < 20000) return configCache.value;
  const items = await listItems('config/');
  let value = { ...DEFAULT_CONFIG };
  if (items.length) {
    items.sort((a, b) => b.uploadedAt - a.uploadedAt);
    const data = await readItem(items[0]);
    if (data) value = { ...DEFAULT_CONFIG, ...data };
    // limpa versões antigas (mantém as 3 últimas)
    if (items.length > 3) deleteItems(items.slice(3)).catch(() => {});
  }
  configCache = { at: Date.now(), value };
  return value;
}

export async function saveConfig(cfg) {
  const value = { ...DEFAULT_CONFIG, ...cfg, savedAt: new Date().toISOString() };
  await writeJson('config/current.json', value);
  configCache = { at: Date.now(), value };
  return value;
}

// ---------- Votos ----------
export function voterKey(name) {
  return normalize(name).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60) || 'anonimo';
}

export function normalize(s) {
  return String(s || '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim();
}

export async function saveBallot(ballot) {
  const key = voterKey(ballot.voter);
  await writeJson(`votes/${key}.json`, { ...ballot, key, savedAt: new Date().toISOString() });
}

// Retorna a cédula mais recente de cada eleitor.
export async function getBallots() {
  const items = await listItems('votes/');
  const latest = latestByKey(items.map((it) => ({
    ...it,
    // votes/<key>-<sufixo>.json  ->  chave votes/<key>
    pathname: it.pathname.replace(/-[A-Za-z0-9]+\.json$/, ''),
  })));
  const ballots = await Promise.all([...latest.values()].map((it) => readItem(it).catch(() => null)));
  // apaga versões antigas em segundo plano
  const keep = new Set([...latest.values()].map((x) => x.ref));
  const old = items.filter((x) => !keep.has(x.ref));
  if (old.length) deleteItems(old).catch(() => {});
  return ballots.filter(Boolean);
}

export async function deleteAllVotes() {
  const items = await listItems('votes/');
  await deleteItems(items);
  return items.length;
}
