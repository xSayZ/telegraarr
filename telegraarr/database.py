import aiosqlite
from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id      INTEGER PRIMARY KEY,
                telegram_name    TEXT,
                jellyseerr_email TEXT,
                approved         INTEGER DEFAULT 0,
                created_at       TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS pending (
                telegram_id      INTEGER PRIMARY KEY,
                telegram_name    TEXT,
                jellyseerr_email TEXT,
                requested_at     TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS failed_attempts (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id      INTEGER,
                telegram_name    TEXT,
                attempted_email  TEXT,
                attempted_at     TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS blocked_users (
                telegram_id      INTEGER PRIMARY KEY,
                telegram_name    TEXT,
                blocked_at       TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.commit()


async def add_pending(telegram_id: int, telegram_name: str, jellyseerr_email: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO pending (telegram_id, telegram_name, jellyseerr_email)
            VALUES (?, ?, ?)
        """, (telegram_id, telegram_name, jellyseerr_email))
        await db.commit()


async def get_pending(telegram_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM pending WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def approve_user(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        # Move from pending to users
        async with db.execute(
            "SELECT * FROM pending WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()

        if row:
            await db.execute("""
                INSERT OR REPLACE INTO users (telegram_id, telegram_name, jellyseerr_email, approved)
                VALUES (?, ?, ?, 1)
            """, (row[0], row[1], row[2]))
            await db.execute("DELETE FROM pending WHERE telegram_id = ?", (telegram_id,))
            await db.commit()
            return True
        return False


async def deny_user(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM pending WHERE telegram_id = ?", (telegram_id,))
        await db.commit()


async def get_user(telegram_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE telegram_id = ? AND approved = 1", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def is_approved(telegram_id: int) -> bool:
    return await get_user(telegram_id) is not None


async def get_failed_attempts(telegram_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM failed_attempts WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def add_failed_attempt(telegram_id: int, telegram_name: str, attempted_email: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO failed_attempts (telegram_id, telegram_name, attempted_email)
            VALUES (?, ?, ?)
        """, (telegram_id, telegram_name, attempted_email))
        await db.commit()


async def is_blocked(telegram_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT blocked FROM blocked_users WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return bool(row) if row else False


async def block_user(telegram_id: int, telegram_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO blocked_users (telegram_id, telegram_name)
            VALUES (?, ?)
        """, (telegram_id, telegram_name))
        await db.commit()


async def unblock_user(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM blocked_users WHERE telegram_id = ?", (telegram_id,)
        )
        await db.commit()