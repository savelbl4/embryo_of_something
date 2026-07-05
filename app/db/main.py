import sqlite3
from datetime import datetime
from pathlib import Path
from app.db.users import init_db_users
from app.db.stickers import init_db_stickers


DB_PATH = Path("/storage/bot.db")


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    init_db_users()
    init_db_stickers()


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
