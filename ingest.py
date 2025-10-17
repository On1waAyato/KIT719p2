import os, yaml
from typing import List, Dict
from pypdf import PdfReader
from rag import RAGIndexer

def load_config():
    with open("config.yml", "r") as f:
        return yaml.safe_load(f)

def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for i, page in enumerate(reader.pages):
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            texts.append("")
    return "\n".join(texts)

def simple_chunk(text: str, chunk_size: int, overlap: int) -> List[str]:
    tokens = text.split()
    chunks = []
    i = 0
    step = max(1, chunk_size - overlap)
    while i < len(tokens):
        chunk_tokens = tokens[i:i+chunk_size]
        chunks.append(" ".join(chunk_tokens))
        i += step
    return chunks

if __name__ == "__main__":
    cfg = load_config()
    rag_cfg = cfg["rag"]
    data_dir = "data"
    pdfs = [p for p in os.listdir(data_dir) if p.lower().endswith(".pdf")]
    if not pdfs:
        print("Place your OSCA PDF(s) in ./data first. See README.md for the link.")
        raise SystemExit(1)

    all_chunks: List[Dict[str, str]] = []
    for pdf in pdfs:
        full = os.path.join(data_dir, pdf)
        print(f"Reading {full} ...")
        raw = read_pdf(full)
        pieces = simple_chunk(raw, rag_cfg["chunk_size"], rag_cfg["chunk_overlap"])
        for j, piece in enumerate(pieces):
            source_id = f"{pdf}#chunk{j+1}"
            all_chunks.append({"source_id": source_id, "text": piece})

    indexer = RAGIndexer(rag_cfg["embedding_model"], rag_cfg["index_dir"])
    print(f"Embedding {len(all_chunks)} chunks and building FAISS index ...")
    indexer.build(all_chunks)
    print("Done. Index saved to:", rag_cfg["index_dir"])
