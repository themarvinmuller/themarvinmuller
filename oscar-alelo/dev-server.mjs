// Servidor local: serve public/ e as funções de api/ (mesmo formato da Vercel).
// Uso: npm run dev  ->  http://localhost:3000  (senha do admin local: "admin")
import http from 'node:http';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const PORT = process.env.PORT || 3000;
const PUB = path.resolve('public');
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon', '.json': 'application/json' };

http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  try {
    if (url.pathname.startsWith('/api/')) {
      const file = path.resolve('.' + url.pathname + '.js');
      const mod = await import(pathToFileURL(file).href + '?t=' + Date.now());
      const handler = mod[req.method];
      if (!handler) { res.writeHead(405); return res.end(); }
      const chunks = [];
      for await (const c of req) chunks.push(c);
      const request = new Request(url, { method: req.method, headers: req.headers, body: ['GET', 'HEAD'].includes(req.method) ? undefined : Buffer.concat(chunks) });
      const r = await handler(request);
      res.writeHead(r.status, Object.fromEntries(r.headers));
      return res.end(Buffer.from(await r.arrayBuffer()));
    }
    let p = url.pathname === '/' ? '/index.html' : url.pathname;
    if (!path.extname(p)) p += '.html';
    const data = await fs.readFile(path.join(PUB, p));
    res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' });
    res.end(data);
  } catch (e) {
    if (e.code !== 'ENOENT' && e.code !== 'ERR_MODULE_NOT_FOUND') console.error(e);
    res.writeHead(e.code === 'ENOENT' || e.code === 'ERR_MODULE_NOT_FOUND' ? 404 : 500);
    res.end(String(e.code || 'erro'));
  }
}).listen(PORT, () => console.log(`Oscar em http://localhost:${PORT}`));
