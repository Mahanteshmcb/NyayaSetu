"""Embedding adapter: sentence-transformers when available, deterministic fallback for tests."""
import hashlib, math, os
_model = None

def encode_text(text: str):
    global _model
    model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    try:
        from sentence_transformers import SentenceTransformer
        if _model is None:
            _model = SentenceTransformer(model_name)
        return _model.encode(text, normalize_embeddings=True).tolist()
    except Exception:
        # Stable feature-hash vector lets the demo run offline. Not semantic-quality embeddings.
        dims = 384
        vector = [0.0] * dims
        tokens = text.lower().split()
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            idx = int.from_bytes(digest[:4], "little") % dims
            vector[idx] += 1.0 if digest[4] % 2 else -1.0
        norm = math.sqrt(sum(v*v for v in vector)) or 1.0
        return [v / norm for v in vector]
