from fastapi import APIRouter, Body
from app.core.vectorstore import VectorStore
from app.core.embeddings import EmbeddingClient
from app.core.llm_client import LLMClient
import os

router = APIRouter()

vectorstore = VectorStore(index_path="data/faiss_index")
embedding_client = EmbeddingClient()
llm_client = LLMClient()


@router.post("/generate_test_cases")
async def generate_test_cases(query: dict = Body(...)):
    user_query = query.get("query", "")
    if not user_query:
        return []

    q_emb = embedding_client.embed_text(user_query)
    hits = vectorstore.query(q_emb, top_k=5)

    test_cases = llm_client.generate_test_cases(user_query, hits)
    return test_cases


@router.post("/generate_selenium")
async def generate_selenium(payload: dict = Body(...)):
    test_case = payload.get("test_case")
    checkout_path = payload.get("checkout_html_path")

    if not test_case or not checkout_path:
        return {"script": "# Missing test_case or checkout_html_path"}

    if not os.path.exists(checkout_path):
        return {"script": f"# checkout.html not found at path: {checkout_path}"}

    with open(checkout_path, "r", encoding="utf-8") as fh:
        html = fh.read()

    query_text = f"{test_case.get('feature', '')} {test_case.get('scenario', '')}"
    q_emb = embedding_client.embed_text(query_text)
    hits = vectorstore.query(q_emb, top_k=5)

    script = llm_client.generate_selenium_script(test_case, html, hits)
    return {"script": script}
