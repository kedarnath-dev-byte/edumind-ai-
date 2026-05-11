"""
@module IngestionController
@description FastAPI router for document ingestion endpoints.
             Persists chunks to a JSON file on disk so they survive
             Render free tier memory resets between requests.
             Follows Controller -> Service -> Repository pattern.
@author      EduMind AI Engineering
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
import json

# ─── Persistent chunk store path ─────────────────────────────────────────────
CHUNK_STORE_PATH = "/tmp/edumind_chunks.json"


def load_chunk_store() -> dict:
    """Load chunks from disk. Returns empty dict if file doesn't exist."""
    try:
        if os.path.exists(CHUNK_STORE_PATH):
            with open(CHUNK_STORE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception:
        return {}


def save_chunk_store(store: dict) -> None:
    """Save chunks to disk."""
    with open(CHUNK_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False)


router = APIRouter(prefix="/api/v1/ingestion", tags=["Ingestion"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF or text document and persist its chunks to disk."""
    try:
        suffix = os.path.splitext(file.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        text = ""
        if suffix.lower() == ".pdf":
            import fitz
            doc = fitz.open(tmp_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        else:
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        os.unlink(tmp_path)

        chunk_size = 500
        overlap = 50
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap

        # Load existing store, add new doc, save back
        store = load_chunk_store()
        store[file.filename] = chunks
        save_chunk_store(store)

        return JSONResponse({
            "status": "success",
            "document_id": file.filename,
            "chunks": len(chunks),
            "message": f"Document ingested with {len(chunks)} chunks"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents")
async def list_documents():
    """List all documents currently stored on disk."""
    try:
        store = load_chunk_store()
        documents = [
            {"document_id": doc_id, "chunks": len(chunks)}
            for doc_id, chunks in store.items()
        ]
        return JSONResponse({"status": "success", "documents": documents})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))