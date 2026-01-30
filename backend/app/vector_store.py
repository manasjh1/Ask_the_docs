import os
import time
import logging
from pinecone import Pinecone, ServerlessSpec
from backend.app.config import settings

logger = logging.getLogger(__name__)

class PineconeStore:
    def __init__(self):
        if not settings.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is missing in .env")

        self.index_name = "ask-the-docs"
        
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)

        existing_indexes = [i.name for i in self.pc.list_indexes()]
        
        if self.index_name not in existing_indexes:
            logger.info(f"Creating new Pinecone index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=384,  
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            while not self.pc.describe_index(self.index_name).status['ready']:
                time.sleep(1)

        self.index = self.pc.Index(self.index_name)

    def add(self, embeddings: list, texts: list, session_id: str):
        """
        Uploads vectors to the specific user's Namespace.
        """
        vectors = []
        for i, (emb, text) in enumerate(zip(embeddings, texts)):
            vector_id = f"{session_id}_{i}"
            
            vectors.append({
                "id": vector_id,
                "values": emb,
                "metadata": {"text": text}  
            })

        self.index.upsert(vectors=vectors, namespace=session_id)

    def search(self, query_embedding: list, session_id: str, top_k: int = 5):
        """
        Searches strictly within the user's namespace.
        """
        try:
            results = self.index.query(
                namespace=session_id,
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            return [
                (match.score, match.metadata["text"]) 
                for match in results.matches
                if match.metadata and "text" in match.metadata
            ]
        except Exception as e:
            logger.error(f"Pinecone search error: {e}")
            return []

    def delete_session(self, session_id: str):
        """
        Clears user data.
        """
        try:
            self.index.delete(delete_all=True, namespace=session_id)
        except Exception:
            pass 