from sentence_transformers import SentenceTransformer
import numpy as np

class MiniLMEmbeddings:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, texts: list[str]) -> np.ndarray:
        """
        Returns normalized embeddings (cosine similarity ready)
        Shape: (n_texts, 384)
        """
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
