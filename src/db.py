import json
import sqlite3
from pathlib import Path

DB_PATH = Path("~/.gcmai_config.db").expanduser()


def setup_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            path TEXT PRIMARY KEY,
            conf TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def save_project_config(path, conf):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO projects (path, conf)
        VALUES (?, ?)
        """,
        (path, json.dumps(conf)),
    )
    conn.commit()
    conn.close()


def is_project_configured(path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT conf FROM projects WHERE path = ?", (path,))
    result = cursor.fetchone()
    conn.close()
    return json.loads(result[0]) if result else None
