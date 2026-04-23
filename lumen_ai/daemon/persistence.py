import sqlite3
import os
import json
from typing import List, Dict, Any

class PersistenceManager:
    """Handles chat history persistence using SQLite."""
    
    def __init__(self):
        # Path: ~/.local/state/lumen-ai/history.db
        state_dir = os.path.expanduser("~/.local/state/lumen-ai")
        os.makedirs(state_dir, exist_ok=True)
        self.db_path = os.path.join(state_dir, "history.db")
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save_message(self, role: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))

    def load_history(self, limit: int = 50) -> List[Dict[str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT role, content FROM messages ORDER BY timestamp DESC LIMIT ?", 
                (limit,)
            )
            rows = cursor.fetchall()
            # Reverse to get chronological order
            return [{"role": r, "content": c} for r, c in reversed(rows)]

    def clear_history(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM messages")
