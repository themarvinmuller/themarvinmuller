export function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...headers },
  });
}

export function isAdmin(request) {
  const expected = process.env.ADMIN_PASSWORD || (process.env.VERCEL ? '' : 'admin');
  const got = request.headers.get('x-admin-password') || '';
  return Boolean(expected) && got === expected;
}

export async function readBody(request) {
  try {
    return await request.json();
  } catch {
    return null;
  }
}
