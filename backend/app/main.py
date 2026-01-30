import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.app.logger import setup_logging
from backend.app.routes import router
import logging

setup_logging()
logger = logging.getLogger(__name__)

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Ask-the-Docs backend started successfully")
    yield

app = FastAPI(title="Ask-the-Docs", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)