from datetime import datetime
from app.db.connection import get_conn


def init_db_users():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_chat_id TEXT UNIQUE,
                tg_user_id TEXT,
                username TEXT,
                first_name TEXT,
                vless_link TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)

def upsert_user(message):
    now = datetime.now().isoformat(timespec="seconds")

    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT id FROM users WHERE tg_user_id = ?",
            (message.from_user.id,)
        )

        existing = cursor.fetchone()

        if existing:
            return False

        conn.execute("""
            INSERT INTO users (
                tg_chat_id,
                tg_user_id,
                username,
                first_name,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(tg_chat_id) DO UPDATE SET
                tg_user_id = excluded.tg_user_id,
                username = excluded.username,
                first_name = excluded.first_name,
                updated_at = excluded.updated_at
        """, (
            str(message.chat.id),
            str(message.from_user.id),
            message.from_user.username,
            message.from_user.first_name,
            now,
            now,
        ))

