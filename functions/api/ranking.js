const ensureSchema = async (db) => {
  await db.prepare(`CREATE TABLE IF NOT EXISTS ranking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    elapsed_ms INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
  )`).run();
};

const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: {
    'content-type': 'application/json; charset=UTF-8',
    'cache-control': 'no-store'
  }
});

export async function onRequestGet({ env }) {
  if (!env.DB) return json({ ok: false, configured: false, ranking: [] }, 503);
  try {
    await ensureSchema(env.DB);
    const { results } = await env.DB.prepare(
      'SELECT name, elapsed_ms AS elapsedMs, created_at AS createdAt FROM ranking ORDER BY elapsed_ms ASC, id ASC LIMIT 100'
    ).all();
    return json({ ok: true, configured: true, ranking: results || [] });
  } catch (error) {
    console.error('Ranking GET error:', error);
    return json({ ok: false, configured: true, ranking: [] }, 500);
  }
}

export async function onRequestPost({ request, env }) {
  if (!env.DB) return json({ ok: false, configured: false, message: 'Ranking global ainda não configurado.' }, 503);

  try {
    const body = await request.json();
    const name = String(body?.name || '').trim().replace(/\s+/g, ' ').slice(0, 30);
    const elapsedMs = Number(body?.elapsedMs);

    if (!name || !Number.isFinite(elapsedMs) || elapsedMs < 0 || elapsedMs > 24 * 60 * 60 * 1000) {
      return json({ ok: false, message: 'Dados de vitória inválidos.' }, 400);
    }

    await ensureSchema(env.DB);
    await env.DB.prepare('INSERT INTO ranking (name, elapsed_ms) VALUES (?, ?)').bind(name.toUpperCase(), Math.round(elapsedMs)).run();
    return json({ ok: true });
  } catch (error) {
    console.error('Ranking POST error:', error);
    return json({ ok: false, configured: true, message: 'Não foi possível registrar a vitória.' }, 500);
  }
}
