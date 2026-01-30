import logging
from backend.app.embeddings import MiniLMEmbeddings
from backend.app.vector_store import PineconeStore
from backend.app.llm import GroqLLM
from backend.app.config import settings

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.embeddings = MiniLMEmbeddings()
        self.llm = GroqLLM()
        self.vector_store = PineconeStore()

        with open(settings.PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()

        logger.info("RAGPipeline initialized with Pinecone")

    def ingest(self, text: str, session_id: str):
        self.vector_store.delete_session(session_id)

        chunks = self._chunk_text(text)
        if not chunks:
            return

        logger.info(f"Ingesting {len(chunks)} chunks for session {session_id}")

        embeddings = self.embeddings.embed(chunks).tolist()
        
        self.vector_store.add(embeddings, chunks, session_id)
        logger.info(f"Upload complete for session {session_id}")

    def query(self, question: str, session_id: str, top_k: int = 5) -> str:
        query_vec = self.embeddings.embed([question])[0].tolist()

        results = self.vector_store.search(query_vec, session_id, top_k)

        filtered_chunks = [text for score, text in results]

        if not filtered_chunks:
            logger.warning("No relevant context found.")
            return "I cannot find the answer in the provided document."

        context = "\n\n".join(filtered_chunks)

        prompt = self.prompt_template.format(context=context, question=question)
        return self.llm.generate(prompt)

    def _chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 150):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        return chunks