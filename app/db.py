import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("/storage/bot.db")


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
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


def set_user_vless_link(chat_id, vless_link):
    now = datetime.now().isoformat(timespec="seconds")

    with get_conn() as conn:
        conn.execute("""
            UPDATE users
            SET vless_link = ?, updated_at = ?
            WHERE tg_chat_id = ?
        """, (vless_link, now, str(chat_id)))


def get_user_vless_link(chat_id):
    with get_conn() as conn:
        row = conn.execute("""
            SELECT vless_link
            FROM users
            WHERE tg_chat_id = ?
        """, (str(chat_id),)).fetchone()

    return row[0] if row else None
