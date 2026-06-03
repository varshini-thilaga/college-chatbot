from typing import List
from sentence_transformers import SentenceTransformer, util
import torch
import re

_embedder = None

def _get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder

def _clean(t): 
    return re.sub(r"\s+", " ", t).strip()

def make_chunks(raw: str, max_chars=300) -> List[str]:
    if not raw or not raw.strip():
        return ["No content available"]
    
    paras = [p.strip() for p in raw.split("\n") if p.strip()]
    if not paras:
        return ["No content available"]
    
    chunks, cur = [], ""
    for p in paras:
        if len(cur) + len(p) + 1 <= max_chars:
            cur += (" " + p) if cur else p
        else:
            if cur.strip():
                chunks.append(_clean(cur))
            cur = p
    if cur.strip():
        chunks.append(_clean(cur))
    if not chunks:
        chunks = ["No content available"]
    
    return chunks

class InMemoryStore:
    def __init__(self, text: str):
        self.chunks = make_chunks(text)
        self.chunks = [chunk for chunk in self.chunks if chunk.strip()]
        if not self.chunks:
            self.chunks = ["No content available"]
        embedder = _get_embedder()
        self.emb = embedder.encode(self.chunks, convert_to_tensor=True)

    def search(self, query: str, top_k=4) -> List[str]:
        if not self.chunks or len(self.chunks) == 0:
            return ["No content available"]
        
        try:
            embedder = _get_embedder()
            q_emb = embedder.encode(query, convert_to_tensor=True)
            scores = util.pytorch_cos_sim(q_emb, self.emb)[0]
            k = min(top_k, len(self.chunks))
            idxs = torch.topk(scores, k=k).indices.tolist()
            return [self.chunks[i] for i in idxs]
        except Exception as e:
            print(f"Search error: {e}")
            return [self.chunks[0] if self.chunks else "Error in search"]
