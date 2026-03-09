from typing import List
from sentence_transformers import SentenceTransformer
from app.config.logger import get_logger

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class EmbeddingError(Exception):
    pass
logger = get_logger(__name__)
_model = None

def get_model():
    global _model
    if _model is None:
        logger.info("[Embedding] Loading embedding model...")
        _model = SentenceTransformer(DEFAULT_EMBEDDING_MODEL)
        logger.info("[Embedding] Embedding model loaded successfully")
    return _model

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []
    
    try:
        non_empty_texts = [text for text in texts if text and text.strip()]
        
        if not non_empty_texts:
            return []
        
        model = get_model()
        embeddings = model.encode(non_empty_texts)
        
        return embeddings.tolist()
    
    except Exception as e:
        raise EmbeddingError(f"Error generating embeddings: {str(e)}")


def generate_embedding(text: str) -> List[float]:
    if not text or not text.strip():
        raise EmbeddingError("Cannot generate embedding for empty text")
    
    embeddings = generate_embeddings([text])
    
    return embeddings[0] if embeddings else []