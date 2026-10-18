import pytest
from fastapi.testclient import TestClient
from server.main import app
from server import db, sync
import os
import shutil

TEST_PROGRAMME_DIR = "test_programme"
db.DB_PATH = "server/data/test_api_programme.db"
sync.PROGRAMME_DIR = TEST_PROGRAMME_DIR

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_teardown():
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    if os.path.exists(TEST_PROGRAMME_DIR):
        shutil.rmtree(TEST_PROGRAMME_DIR)

    os.makedirs(TEST_PROGRAMME_DIR)
    with open(os.path.join(TEST_PROGRAMME_DIR, "00-index.md"), "w") as f:
        f.write("# Index\n\nWelcome.")

    db.init_db()
    sync.sync_all()

    yield

    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    if os.path.exists(TEST_PROGRAMME_DIR):
        shutil.rmtree(TEST_PROGRAMME_DIR)

def test_api_get_documents():
    response = client.get("/api/documents")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) == 1
    assert docs[0]["title"] == "Index"

def test_api_update_document():
    # First get doc id
    docs = client.get("/api/documents").json()
    doc_id = docs[0]["id"]

    # Update content
    new_content = "# Index Updated\n\nNew text."
    response = client.put(f"/api/documents/{doc_id}", json={"content": new_content})
    assert response.status_code == 200

    # Check disk
    with open(os.path.join(TEST_PROGRAMME_DIR, "00-index.md"), "r") as f:
        assert f.read() == new_content

    # Check revisions
    revs = client.get(f"/api/documents/{doc_id}/revisions").json()
    assert len(revs) == 2
    assert revs[0]["content"] == new_content
    assert revs[0]["source"] == "ui_edit"
