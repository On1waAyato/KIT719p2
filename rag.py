import os, json, pickle
from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

@dataclass
class DocChunk:
    source_id: str
    text: str
    embedding: np.ndarray

class RAGIndexer:
    def __init__(self, embedding_model: str, index_dir: str):
        self.index_dir = index_dir
        os.makedirs(index_dir, exist_ok=True)
        self.model = SentenceTransformer(embedding_model)
        self.index = None
        self.meta: List[Dict[str, Any]] = []
        self.dim = self.model.get_sentence_embedding_dimension()

    def _index_paths(self):
        return os.path.join(self.index_dir, "index.faiss"), os.path.join(self.index_dir, "meta.pkl")

    def build(self, chunks: List[Dict[str, str]]):
        embeddings = []
        meta = []
        for ch in chunks:
            emb = self.model.encode(ch["text"], normalize_embeddings=True)
            embeddings.append(emb)
            meta.append({"source_id": ch["source_id"], "text": ch["text"]})
        mat = np.vstack(embeddings).astype("float32")
        index = faiss.IndexFlatIP(mat.shape[1])
        index.add(mat)
        self.index = index
        self.meta = meta
        # persist
        ipath, mpath = self._index_paths()
        faiss.write_index(index, ipath)
        with open(mpath, "wb") as f:
            pickle.dump(meta, f)

    def load(self):
        ipath, mpath = self._index_paths()
        if not (os.path.exists(ipath) and os.path.exists(mpath)):
            raise FileNotFoundError("Index not found. Run ingest.py first.")
        self.index = faiss.read_index(ipath)
        with open(mpath, "rb") as f:
            self.meta = pickle.load(f)
        self.dim = self.index.d

    def retrieve(self, query: str, top_k: int = 4):
        if self.index is None:
            self.load()
        q_emb = self.model.encode(query, normalize_embeddings=True).astype("float32")
        import numpy as np
        D, I = self.index.search(np.expand_dims(q_emb, 0), top_k)
        out = []
        for idx, score in zip(I[0], D[0]):
            if idx == -1:
                continue
            m = self.meta[idx]
            out.append({"source_id": m["source_id"], "text": m["text"], "score": float(score)})
        return out
