CREATE TABLE IF NOT EXISTS ranking (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  elapsed_ms INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_ranking_elapsed ON ranking (elapsed_ms ASC, id ASC);
