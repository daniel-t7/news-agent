import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "news.db"


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


@contextmanager
def _connect():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Липсва базата {DB_PATH}. Създай я с: sqlite3 data/news.db < schema.sql"
        )
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def is_seen(url: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM seen_articles WHERE url = ?", (url,)
        ).fetchone()
        return row is not None


def mark_seen(url: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO seen_articles (url, seen_at) VALUES (?, ?)",
            (url, _now()),
        )


def save_digest(topic: str, content: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO digests (topic, content, created_at) VALUES (?, ?, ?)",
            (topic, content, _now()),
        )


def get_digests(limit: int = 5) -> list[tuple]:
    with _connect() as conn:
        return conn.execute(
            "SELECT created_at, topic, content FROM digests ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
