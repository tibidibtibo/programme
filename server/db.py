import sqlite3
import os
from typing import Dict, Any, List, Optional
import datetime

DB_PATH = "server/data/programme.db"

def get_db() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT UNIQUE,
        title TEXT,
        category TEXT,
        file_hash TEXT,
        file_size INTEGER,
        mtime REAL,
        version_count INTEGER DEFAULT 1,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS revisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER REFERENCES documents(id),
        version_number INTEGER,
        content TEXT,
        file_hash TEXT,
        source TEXT,
        diff_summary TEXT NULL,
        created_at TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        file_path TEXT,
        details TEXT,
        timestamp TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def execute_query(query: str, params: tuple = ()) -> sqlite3.Cursor:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor

def execute_read_query(query: str, params: tuple = ()) -> List[sqlite3.Row]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def get_document_by_path(file_path: str) -> Optional[sqlite3.Row]:
    res = execute_read_query("SELECT * FROM documents WHERE file_path = ?", (file_path,))
    return res[0] if res else None

def get_document_by_id(doc_id: int) -> Optional[sqlite3.Row]:
    res = execute_read_query("SELECT * FROM documents WHERE id = ?", (doc_id,))
    return res[0] if res else None

def add_document(file_path: str, title: str, category: str, file_hash: str, file_size: int, mtime: float) -> int:
    now = datetime.datetime.now().isoformat()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO documents (file_path, title, category, file_hash, file_size, mtime, version_count, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, 1, 1, ?, ?)
    """, (file_path, title, category, file_hash, file_size, mtime, now, now))
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def update_document(doc_id: int, title: str, file_hash: str, file_size: int, mtime: float, is_active: int = 1):
    now = datetime.datetime.now().isoformat()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE documents
        SET title = ?, file_hash = ?, file_size = ?, mtime = ?, is_active = ?, updated_at = ?, version_count = version_count + 1
        WHERE id = ?
    """, (title, file_hash, file_size, mtime, is_active, now, doc_id))
    conn.commit()
    conn.close()

def set_document_inactive(doc_id: int):
    now = datetime.datetime.now().isoformat()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE documents SET is_active = 0, updated_at = ? WHERE id = ?
    """, (now, doc_id))
    conn.commit()
    conn.close()

def add_revision(document_id: int, version_number: int, content: str, file_hash: str, source: str, diff_summary: str = None):
    now = datetime.datetime.now().isoformat()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO revisions (document_id, version_number, content, file_hash, source, diff_summary, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (document_id, version_number, content, file_hash, source, diff_summary, now))
    conn.commit()
    conn.close()

def get_revisions(document_id: int) -> List[sqlite3.Row]:
    return execute_read_query("SELECT * FROM revisions WHERE document_id = ? ORDER BY version_number DESC", (document_id,))

def get_revision(rev_id: int) -> Optional[sqlite3.Row]:
    res = execute_read_query("SELECT * FROM revisions WHERE id = ?", (rev_id,))
    return res[0] if res else None

def get_all_active_documents() -> List[sqlite3.Row]:
    return execute_read_query("SELECT * FROM documents WHERE is_active = 1 ORDER BY category, title")

def log_event(event_type: str, file_path: str, details: str = ""):
    now = datetime.datetime.now().isoformat()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO file_events (event_type, file_path, details, timestamp)
        VALUES (?, ?, ?, ?)
    """, (event_type, file_path, details, now))
    conn.commit()
    conn.close()
