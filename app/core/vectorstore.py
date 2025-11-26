import faiss
import numpy as np
import os
import pickle

class VectorStore:
    def __init__(self, index_path: str = 'data/faiss_index'):
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        self.index_path = index_path
        self.index = None
        self.metadatas = []
        self.dim = 384
        self._load()

    def _load(self):
        if os.path.exists(self.index_path + '.index') and os.path.exists(self.index_path + '.meta'):
            self.index = faiss.read_index(self.index_path + '.index')
            with open(self.index_path + '.meta', 'rb') as fh:
                self.metadatas = pickle.load(fh)
        else:
            self.index = faiss.IndexFlatL2(self.dim)

    def upsert(self, embeddings: list, metas: list):
        embs = [e['embedding'] for e in embeddings]
        arr = np.vstack(embs).astype('float32')
        self.index.add(arr)
        for m, t in zip(metas, embeddings):
            md = {"source": m['source'], "text": t['metadata'].get('text','')}
            self.metadatas.append(md)
        faiss.write_index(self.index, self.index_path + '.index')
        with open(self.index_path + '.meta', 'wb') as fh:
            pickle.dump(self.metadatas, fh)

    def query(self, query_embedding, top_k: int = 5):
        import numpy as np
        q = np.array([query_embedding]).astype('float32')
        if self.index.ntotal == 0:
            return []
        D, I = self.index.search(q, top_k)
        results = []
        for idx in I[0]:
            md = self.metadatas[idx]
            results.append({"score": 0.0, "metadata": md, "text": md.get('text','')})
        return results
