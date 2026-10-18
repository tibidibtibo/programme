import os
import hashlib
from typing import Dict, Any, List
from server import db

PROGRAMME_DIR = "programme"

def compute_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def extract_title(content_str: str) -> str:
    for line in content_str.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    return "Sans titre"

def categorize(file_path: str) -> str:
    parts = file_path.split(os.sep)
    if len(parts) == 2:
        return "racine"
    if "domaines" in parts:
        return "domaines"
    if "annexes" in parts:
        return "annexes"
    if "lots" in parts:
        return "lots"
    if "audit" in parts:
        return "audit"
    return "autre"

def sync_all() -> Dict[str, List[str]]:
    changes = {"created": [], "modified": [], "deleted": [], "moved": []}

    # 1. Gather files on disk
    disk_files = {}
    for root, _, files in os.walk(PROGRAMME_DIR):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                # Ensure using consistent paths
                norm_path = os.path.normpath(full_path).replace("\\", "/")
                stat = os.stat(norm_path)

                with open(norm_path, 'rb') as f:
                    content_bytes = f.read()

                file_hash = compute_hash(content_bytes)

                disk_files[norm_path] = {
                    "size": stat.st_size,
                    "mtime": stat.st_mtime,
                    "hash": file_hash,
                    "content": content_bytes.decode('utf-8', errors='replace')
                }

    # 2. Gather active DB files
    db_docs = db.get_all_active_documents()
    db_files = {doc["file_path"]: doc for doc in db_docs}

    # 3. Detect Deletions & Moves
    for db_path in list(db_files.keys()):
        doc = db_files[db_path]
        if db_path not in disk_files:
            # File missing on disk. Was it moved?
            moved_to = None
            for dp, df_info in disk_files.items():
                if dp not in db_files and df_info["hash"] == doc["file_hash"]:
                    moved_to = dp
                    break

            if moved_to:
                # Update path (and also ensure it doesn't cause integrity error if moved_to exists in DB, though we already filtered active docs)
                # Ensure moved_to doesn't already exist in db_files
                existing_doc_at_new_path = db.get_document_by_path(moved_to)
                if existing_doc_at_new_path:
                    # If it already exists and is active, something is strange (maybe overlapping move).
                    # Set the existing one to inactive before moving.
                    db.set_document_inactive(existing_doc_at_new_path["id"])

                conn = db.get_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE documents SET file_path = ?, is_active = 1 WHERE id = ?", (moved_to, doc["id"]))
                conn.commit()
                conn.close()
                db.log_event("moved", f"{db_path} -> {moved_to}")
                changes["moved"].append(f"{db_path} -> {moved_to}")
                # We artificially say this path is now in db_files to avoid re-adding
                db_files[moved_to] = dict(doc)
                db_files[moved_to]["file_path"] = moved_to
                del db_files[db_path]
            else:
                db.set_document_inactive(doc["id"])
                db.log_event("deleted", db_path)
                changes["deleted"].append(db_path)

    # 4. Detect Creations & Modifications
    for dp, df_info in disk_files.items():
        if dp not in db_files:
            # Check if this file was previously in DB (but inactive)
            existing_doc = db.get_document_by_path(dp)
            title = extract_title(df_info["content"])
            category = categorize(dp)
            if existing_doc:
                # File path was used before. Update it and make it active again.
                db.update_document(existing_doc["id"], title, df_info["hash"], df_info["size"], df_info["mtime"], is_active=1)

                updated_doc = db.get_document_by_id(existing_doc["id"])
                v_num = updated_doc["version_count"]

                db.add_revision(existing_doc["id"], v_num, df_info["content"], df_info["hash"], "disk_change", "Recreated file")
                db.log_event("created", dp, "Recreated")
                changes["created"].append(dp)
            else:
                # Completely new file
                doc_id = db.add_document(dp, title, category, df_info["hash"], df_info["size"], df_info["mtime"])
                db.add_revision(doc_id, 1, df_info["content"], df_info["hash"], "initial_scan")
                db.log_event("created", dp)
                changes["created"].append(dp)
        else:
            doc = db_files[dp]
            if doc["file_hash"] != df_info["hash"] or doc["mtime"] != df_info["mtime"]:
                title = extract_title(df_info["content"])
                db.update_document(doc["id"], title, df_info["hash"], df_info["size"], df_info["mtime"])

                # Fetch new version count
                updated_doc = db.get_document_by_id(doc["id"])
                v_num = updated_doc["version_count"]

                db.add_revision(doc["id"], v_num, df_info["content"], df_info["hash"], "disk_change")
                db.log_event("modified", dp)
                changes["modified"].append(dp)

    return changes
