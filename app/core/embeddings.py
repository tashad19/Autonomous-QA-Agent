from sentence_transformers import SentenceTransformer

class EmbeddingClient:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.embeddings = []

    def embed_text(self, text: str):
        return self.model.encode(text, show_progress_bar=False)

    def build_embeddings(self, texts: list, metas: list):
        embs = self.model.encode(texts, show_progress_bar=True)
        self.embeddings = []
        for e, m, t in zip(embs, metas, texts):
            self.embeddings.append({"embedding": e, "metadata": {"source": m['source'], "text": t}})
