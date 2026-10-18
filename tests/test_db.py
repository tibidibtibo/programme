import pytest
import os
from server import db

@pytest.fixture(autouse=True)
def setup_db():
    db.DB_PATH = "server/data/test_programme.db"
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()
    yield
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)

def test_db_operations():
    doc_id = db.add_document("test.md", "Test", "domaines", "hash1", 100, 1000.0)
    assert doc_id is not None

    doc = db.get_document_by_id(doc_id)
    assert doc["title"] == "Test"

    db.add_revision(doc_id, 1, "# Test", "hash1", "initial_scan")

    revs = db.get_revisions(doc_id)
    assert len(revs) == 1
    assert revs[0]["content"] == "# Test"

    db.update_document(doc_id, "Test 2", "hash2", 150, 2000.0)
    doc2 = db.get_document_by_id(doc_id)
    assert doc2["title"] == "Test 2"
    assert doc2["version_count"] == 2
