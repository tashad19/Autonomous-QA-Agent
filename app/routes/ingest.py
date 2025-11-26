from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.core.embeddings import EmbeddingClient
from app.core.vectorstore import VectorStore
from app.core.html_parser import parse_html_text
import os

router = APIRouter()

embedding_client = EmbeddingClient()
vectorstore = VectorStore(index_path="data/faiss_index")

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...), checkout_html: UploadFile = File(None)):
    saved = []
    os.makedirs("uploads", exist_ok=True)
    for f in files:
        path = os.path.join("uploads", f.filename)
        with open(path, "wb") as out:
            out.write(await f.read())
        saved.append(path)
    if checkout_html:
        ch_path = os.path.join("uploads", checkout_html.filename)
        with open(ch_path, "wb") as out:
            out.write(await checkout_html.read())
        saved.append(ch_path)
    docs = []
    for path in saved:
        if path.endswith('.html'):
            text = parse_html_text(path)
        else:
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    text = fh.read()
            except Exception:
                text = ''
        if text:
            docs.append({"path": path, "text": text})
    texts = [d['text'] for d in docs]
    metas = [{"source": d['path']} for d in docs]
    embedding_client.build_embeddings(texts, metas)
    vectorstore.upsert(embedding_client.embeddings, metas)
    return JSONResponse({"message": "Knowledge Base Built", "files": saved})
