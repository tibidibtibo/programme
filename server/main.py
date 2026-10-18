from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import markdown
import os
import re
from contextlib import asynccontextmanager
from typing import List, Optional

from server import db, sync

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: init DB and run sync
    db.init_db()
    sync.sync_all()
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan, title="Programme Editor")

app.mount("/static", StaticFiles(directory="server/static"), name="static")
templates = Jinja2Templates(directory="server/templates")

# Configure Markdown
md_extensions = ['tables', 'fenced_code', 'toc', 'attr_list', 'def_list', 'sane_lists', 'md_in_html']

def render_markdown(text: str) -> str:
    # Insérer une ligne vide avant les listes pour un rendu GFM aéré et propre
    text = re.sub(r'([^\n])\n([ \t]*([0-9]+\.|[-*+])\s+)', r'\1\n\n\2', text)
    lines = text.split('\n')
    processed_lines = []
    in_alert = False
    for line in lines:
        m = re.match(r'^>\s*\[!([A-Za-z_-]+)\](.*)$', line)
        if m:
            alert_type = m.group(1).lower()
            extra = m.group(2).strip()
            processed_lines.append(f'<div class="alert alert-{alert_type}">')
            if extra:
                processed_lines.append(f'<p>{extra}</p>')
            in_alert = True
        elif in_alert and not line.startswith(">"):
            processed_lines.append('</div>')
            processed_lines.append(line)
            in_alert = False
        elif in_alert and line.startswith(">"):
            processed_lines.append(line[1:].strip())
        else:
            processed_lines.append(line)
    if in_alert:
        processed_lines.append('</div>')

    return markdown.markdown('\n'.join(processed_lines), extensions=md_extensions)

# Models
class UpdateContentRequest(BaseModel):
    content: str

class RenderRequest(BaseModel):
    content: str

# API Endpoints
@app.get("/api/documents")
def get_documents():
    docs = db.get_all_active_documents()
    return [dict(d) for d in docs]

@app.get("/api/documents/{doc_id}")
def get_document(doc_id: int):
    doc = db.get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get latest revision for content
    revs = db.get_revisions(doc_id)
    content = revs[0]["content"] if revs else ""
    html = render_markdown(content)

    res = dict(doc)
    res["content"] = content
    res["html"] = html
    return res

@app.post("/api/render")
def render_md(req: RenderRequest):
    return {"html": render_markdown(req.content)}

@app.put("/api/documents/{doc_id}")
def update_document(doc_id: int, req: UpdateContentRequest):
    doc = db.get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Write to disk
    file_path = doc["file_path"]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(req.content)

    # Re-sync specific file manually or run global sync
    # For speed, we just run sync_all() but ideally we'd just update this one
    content_bytes = req.content.encode('utf-8')
    file_hash = sync.compute_hash(content_bytes)
    stat = os.stat(file_path)
    title = sync.extract_title(req.content)

    db.update_document(doc_id, title, file_hash, stat.st_size, stat.st_mtime)

    # Need to fetch doc again to get updated version count
    updated_doc = db.get_document_by_id(doc_id)

    db.add_revision(doc_id, updated_doc["version_count"], req.content, file_hash, "ui_edit")
    db.log_event("modified", file_path, "via UI")

    return {"status": "success", "version": updated_doc["version_count"]}

@app.get("/api/documents/{doc_id}/revisions")
def get_document_revisions(doc_id: int):
    revs = db.get_revisions(doc_id)
    return [dict(r) for r in revs]

@app.get("/api/documents/{doc_id}/revisions/{rev_id}")
def get_document_revision(doc_id: int, rev_id: int):
    rev = db.get_revision(rev_id)
    if not rev or rev["document_id"] != doc_id:
        raise HTTPException(status_code=404, detail="Revision not found")
    return dict(rev)

@app.post("/api/documents/{doc_id}/restore/{rev_id}")
def restore_revision(doc_id: int, rev_id: int):
    doc = db.get_document_by_id(doc_id)
    rev = db.get_revision(rev_id)
    if not doc or not rev or rev["document_id"] != doc_id:
        raise HTTPException(status_code=404, detail="Not found")

    # Write old content to disk
    with open(doc["file_path"], "w", encoding="utf-8") as f:
        f.write(rev["content"])

    content_bytes = rev["content"].encode('utf-8')
    file_hash = sync.compute_hash(content_bytes)
    stat = os.stat(doc["file_path"])
    title = sync.extract_title(rev["content"])

    db.update_document(doc_id, title, file_hash, stat.st_size, stat.st_mtime)
    updated_doc = db.get_document_by_id(doc_id)

    db.add_revision(doc_id, updated_doc["version_count"], rev["content"], file_hash, "restore", f"Restored from v{rev['version_number']}")

    return {"status": "success", "version": updated_doc["version_count"]}

@app.post("/api/sync")
def trigger_sync():
    changes = sync.sync_all()
    return changes

# UI Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/{path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, path: str):
    # This enables refreshing on any virtual URL
    if path.startswith("api/") or path.startswith("static/"):
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(request=request, name="index.html")

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=True)
