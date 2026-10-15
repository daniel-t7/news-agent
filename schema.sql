CREATE TABLE seen_articles (
    url TEXT PRIMARY KEY,
    seen_at TEXT NOT NULL
);

CREATE TABLE digests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
);
