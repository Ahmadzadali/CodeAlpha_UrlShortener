import sqlite3
from config import DATABASE_NAME


def get_connection():
  conn = sqlite3.connect(DATABASE_NAME)
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  with get_connection() as conn:
    conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_url(short_code: str, original_url: str):
  with get_connection() as conn:
    conn.execute(
        "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
        (short_code, original_url),
    )


def get_by_short_code(short_code: str):
  with get_connection() as conn:
    return conn.execute(
        "SELECT * FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()


def get_by_original_url(original_url: str):
  with get_connection() as conn:
    return conn.execute(
        "SELECT * FROM urls WHERE original_url = ?", (original_url,)
    ).fetchone()


def increment_clicks(short_code: str):
  with get_connection() as conn:
    conn.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
        (short_code,),
    )