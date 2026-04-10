import os
import json
import aiosqlite
from datetime import datetime

DB_PATH = None


async def init_db(db_path: str):
    """spin up the sqlite db and create tables if they don't exist yet"""
    global DB_PATH
    DB_PATH = db_path

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                track TEXT NOT NULL,
                module TEXT NOT NULL,
                lesson_completed BOOLEAN DEFAULT 0,
                scenarios_completed TEXT DEFAULT '[]',
                started_at TEXT,
                completed_at TEXT,
                UNIQUE(track, module)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS scenario_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_id TEXT UNIQUE NOT NULL,
                track TEXT NOT NULL,
                module TEXT NOT NULL,
                status TEXT DEFAULT 'ready',
                started_at TEXT,
                completed_at TEXT,
                attempts INTEGER DEFAULT 0
            )
        """)
        await db.commit()


async def get_progress(track: str = None):
    """grab progress rows, optionally filtered by track"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if track:
            cursor = await db.execute(
                "SELECT * FROM progress WHERE track = ?", (track,)
            )
        else:
            cursor = await db.execute("SELECT * FROM progress")
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def update_progress(track: str, module: str, **kwargs):
    """upsert a progress row -- pass whatever fields you want to update"""
    async with aiosqlite.connect(DB_PATH) as db:
        existing = await db.execute(
            "SELECT id FROM progress WHERE track = ? AND module = ?",
            (track, module),
        )
        row = await existing.fetchone()

        if row:
            sets = ", ".join(f"{k} = ?" for k in kwargs)
            values = list(kwargs.values()) + [track, module]
            await db.execute(
                f"UPDATE progress SET {sets} WHERE track = ? AND module = ?",
                values,
            )
        else:
            kwargs.update({
                "track": track,
                "module": module,
                "started_at": datetime.now().isoformat(),
            })
            cols = ", ".join(kwargs.keys())
            placeholders = ", ".join("?" * len(kwargs))
            await db.execute(
                f"INSERT INTO progress ({cols}) VALUES ({placeholders})",
                list(kwargs.values()),
            )
        await db.commit()


async def get_scenario_state(scenario_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM scenario_state WHERE scenario_id = ?", (scenario_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None


async def update_scenario_state(scenario_id: str, **kwargs):
    async with aiosqlite.connect(DB_PATH) as db:
        existing = await db.execute(
            "SELECT id FROM scenario_state WHERE scenario_id = ?", (scenario_id,)
        )
        row = await existing.fetchone()

        if row:
            sets = ", ".join(f"{k} = ?" for k in kwargs)
            values = list(kwargs.values()) + [scenario_id]
            await db.execute(
                f"UPDATE scenario_state SET {sets} WHERE scenario_id = ?",
                values,
            )
        else:
            kwargs["scenario_id"] = scenario_id
            cols = ", ".join(kwargs.keys())
            placeholders = ", ".join("?" * len(kwargs))
            await db.execute(
                f"INSERT INTO scenario_state ({cols}) VALUES ({placeholders})",
                list(kwargs.values()),
            )
        await db.commit()


async def get_active_scenarios():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM scenario_state WHERE status = 'active'"
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def clear_all_progress():
    """nuke everything -- used by training-lab reset"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM progress")
        await db.execute("DELETE FROM scenario_state")
        await db.commit()
