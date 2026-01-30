from backend.app.embeddings import MiniLMEmbeddings

def test_embedding_dimension():
    # This runs the REAL embedding model
    emb = MiniLMEmbeddings().embed(["hello"])
    
    # Check if we get a numpy array
    assert hasattr(emb, "shape")
    
    # Check if dimension is correct (384 for MiniLM-L6-v2)
    assert emb.shape[1] == 384