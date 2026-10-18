import pytest
import os
import shutil
from server import db, sync

TEST_PROGRAMME_DIR = "test_programme"

@pytest.fixture(autouse=True)
def setup_teardown():
    sync.PROGRAMME_DIR = TEST_PROGRAMME_DIR
    db.DB_PATH = "server/data/test_programme.db"

    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()

    if os.path.exists(TEST_PROGRAMME_DIR):
        shutil.rmtree(TEST_PROGRAMME_DIR)
    os.makedirs(TEST_PROGRAMME_DIR)
    os.makedirs(os.path.join(TEST_PROGRAMME_DIR, "domaines"))

    yield

    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    if os.path.exists(TEST_PROGRAMME_DIR):
        shutil.rmtree(TEST_PROGRAMME_DIR)

def test_sync_all():
    # 1. Create file
    fpath = os.path.join(TEST_PROGRAMME_DIR, "domaines", "01-test.md")
    with open(fpath, "w") as f:
        f.write("# Titre 1\nContenu 1")

    changes = sync.sync_all()
    assert len(changes["created"]) == 1
    assert "modified" not in changes or len(changes["modified"]) == 0

    doc = db.get_document_by_path(fpath.replace("\\", "/"))
    assert doc is not None
    assert doc["title"] == "Titre 1"

    # 2. Modify file
    with open(fpath, "w") as f:
        f.write("# Titre 2\nContenu 2")

    changes = sync.sync_all()
    assert len(changes["modified"]) == 1

    doc2 = db.get_document_by_path(fpath.replace("\\", "/"))
    assert doc2["title"] == "Titre 2"
    assert doc2["version_count"] == 2

    # 3. Move file
    fpath_new = os.path.join(TEST_PROGRAMME_DIR, "domaines", "02-test-moved.md")
    os.rename(fpath, fpath_new)

    changes = sync.sync_all()
    assert len(changes["moved"]) == 1

    doc_moved = db.get_document_by_path(fpath_new.replace("\\", "/"))
    assert doc_moved is not None
    assert db.get_document_by_path(fpath.replace("\\", "/")) is None

    # 4. Delete file
    os.remove(fpath_new)
    changes = sync.sync_all()
    assert len(changes["deleted"]) == 1

    doc_deleted = db.get_document_by_id(doc_moved["id"])
    assert doc_deleted["is_active"] == 0
