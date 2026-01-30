from fastapi import APIRouter, UploadFile, File, HTTPException, Header
import pdfplumber
from backend.app.rag import RAGPipeline

router = APIRouter()
rag = RAGPipeline()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    x_session_id: str = Header(...)
):
    text = ""

    # 1. Read File
    if file.filename.lower().endswith(".txt"):
        content = await file.read()
        text = content.decode("utf-8", errors="ignore")
    elif file.filename.lower().endswith(".pdf"):
        try:
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to read PDF")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found")

    # 2. Process Sync (Wait for it to finish)
    rag.ingest(text, x_session_id)

    return {
        "status": "success",
        "filename": file.filename,
        "session_id": x_session_id
    }

@router.post("/query")
def ask_question(
    payload: dict,
    x_session_id: str = Header(...)
):
    question = payload.get("question")
    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Question is required")

    answer = rag.query(question, x_session_id)
    print(f"\n💡 LLM ANSWER (Session {x_session_id}): {answer}\n")
    return {"answer": answer}