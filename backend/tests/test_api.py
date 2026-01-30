from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.app.main import app    

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

@patch("backend.app.routes.rag")
def test_upload_txt_file(mock_rag):
    # Setup the mock
    mock_rag.ingest = MagicMock()

    # Create a fake text file
    file_content = b"This is a test document content."
    files = {"file": ("test_doc.txt", file_content, "text/plain")}
    
    # Send request
    res = client.post("/documents/upload", files=files)
    
    # Verify response
    assert res.status_code == 200
    assert res.json() == {
        "status": "processing_started",
        "filename": "test_doc.txt"
    }
    
    mock_rag.ingest.assert_called_once()

# 3. Test Query Endpoint
@patch("backend.app.routes.rag")
def test_query(mock_rag):
    # Setup the mock to return a fake answer
    mock_rag.query.return_value = "This is a test answer from the LLM."
    
    payload = {"question": "What is this?", "top_k": 2}
    res = client.post("/query", json=payload)
    
    assert res.status_code == 200
    assert res.json()["answer"] == "This is a test answer from the LLM."
    
    # Verify the query method was called with correct arguments
    mock_rag.query.assert_called_once_with("What is this?", 2)

# 4. Test Query with Missing Question
def test_query_invalid():
    payload = {"question": "", "top_k": 2}
    res = client.post("/query", json=payload)
    
    assert res.status_code == 400
    assert res.json()["detail"] == "Question is required"