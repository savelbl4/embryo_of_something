from datetime import datetime, timedelta
import secrets
import string

from app.db.connection import get_conn


def init_db_bridge():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS identities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                platform TEXT NOT NULL,
                platform_user_id TEXT NOT NULL,
                platform_chat_id TEXT,
                username TEXT,
                display_name TEXT,

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,

                UNIQUE(platform, platform_user_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS identity_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                identity_id_1 INTEGER NOT NULL,
                identity_id_2 INTEGER NOT NULL,

                created_at TEXT NOT NULL,

                UNIQUE(identity_id_1, identity_id_2),

                FOREIGN KEY(identity_id_1) REFERENCES identities(id),
                FOREIGN KEY(identity_id_2) REFERENCES identities(id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS link_codes (
                code TEXT PRIMARY KEY,

                identity_id INTEGER NOT NULL,
                expires_at TEXT NOT NULL,

                FOREIGN KEY(identity_id) REFERENCES identities(id)
            )
        """)

        conn.commit()


def upsert_identity(
    platform: str,
    platform_user_id: str,
    platform_chat_id: str | None = None,
    username: str | None = None,
    display_name: str | None = None,
) -> int:
    now = datetime.now().isoformat(timespec="seconds")

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO identities (
                platform,
                platform_user_id,
                platform_chat_id,
                username,
                display_name,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(platform, platform_user_id) DO UPDATE SET
                platform_chat_id = excluded.platform_chat_id,
                username = excluded.username,
                display_name = excluded.display_name,
                updated_at = excluded.updated_at
        """, (
            platform,
            str(platform_user_id),
            str(platform_chat_id) if platform_chat_id is not None else None,
            username,
            display_name,
            now,
            now,
        ))

        row = conn.execute("""
            SELECT id
            FROM identities
            WHERE platform = ? AND platform_user_id = ?
        """, (
            platform,
            str(platform_user_id),
        )).fetchone()

        conn.commit()
        return row["id"]


def generate_link_code(identity_id: int, ttl_minutes: int = 10) -> str:
    alphabet = string.ascii_uppercase + string.digits
    code = "".join(secrets.choice(alphabet) for _ in range(6))

    expires_at = (datetime.now() + timedelta(minutes=ttl_minutes)).isoformat(timespec="seconds")

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO link_codes (
                code,
                identity_id,
                expires_at
            )
            VALUES (?, ?, ?)
        """, (
            code,
            identity_id,
            expires_at,
        ))

        conn.commit()

    return code


def link_by_code(target_identity_id: int, code: str) -> bool:
    now = datetime.now().isoformat(timespec="seconds")
    code = code.strip().upper()

    with get_conn() as conn:
        row = conn.execute("""
            SELECT identity_id
            FROM link_codes
            WHERE code = ?
              AND expires_at > ?
        """, (
            code,
            now,
        )).fetchone()

        if not row:
            return False

        source_identity_id = row["identity_id"]

        if source_identity_id == target_identity_id:
            return False

        a, b = sorted([source_identity_id, target_identity_id])

        conn.execute("""
            INSERT OR IGNORE INTO identity_links (
                identity_id_1,
                identity_id_2,
                created_at
            )
            VALUES (?, ?, ?)
        """, (
            a,
            b,
            now,
        ))

        conn.execute("""
            DELETE FROM link_codes
            WHERE code = ?
        """, (
            code,
        ))

        conn.commit()
        return True


def get_linked_identity(identity_id: int, target_platform: str):
    with get_conn() as conn:
        row = conn.execute("""
            SELECT i.*
            FROM identity_links l
            JOIN identities i
              ON i.id = CASE
                  WHEN l.identity_id_1 = ? THEN l.identity_id_2
                  ELSE l.identity_id_1
              END
            WHERE ? IN (l.identity_id_1, l.identity_id_2)
              AND i.platform = ?
            LIMIT 1
        """, (
            identity_id,
            identity_id,
            target_platform,
        )).fetchone()

    return row
