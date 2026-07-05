from datetime import datetime
from app.db.connection import get_conn

def init_db_stickers():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stickers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT NOT NULL UNIQUE,
                file_unique_id TEXT NOT NULL,
                emoji TEXT,
                set_name TEXT,
                type TEXT,
                is_animated INTEGER NOT NULL DEFAULT 0,
                is_video INTEGER NOT NULL DEFAULT 0,
                added_at TEXT NOT NULL
            );
        """)
        conn.commit()

def add_sticker_if_not_exists(sticker):
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT id FROM stickers WHERE file_id = ?",
            (sticker.file_id,)
        )

        existing = cursor.fetchone()

        if existing:
            return False

        conn.execute("""
            INSERT INTO stickers (
                file_id,
                file_unique_id,
                emoji,
                set_name,
                type,
                is_animated,
                is_video,
                added_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sticker.file_id,
            sticker.file_unique_id,
            sticker.emoji,
            sticker.set_name,
            sticker.type,
            int(sticker.is_animated),
            int(sticker.is_video),
            datetime.now().isoformat(timespec="seconds"),
        ))

        conn.commit()
        return True

def get_random_sticker():
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT file_id
            FROM stickers
            ORDER BY RANDOM()
            LIMIT 1
        """)
        row = cursor.fetchone()

    return row["file_id"] if row else None
