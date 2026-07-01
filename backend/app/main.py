from fastapi import FastAPI
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from ml_pipeline.config import MODELS_DIR
from backend.app.model_manager import manager
from backend.app.api.routes import router
import joblib
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_models():
    logger.info("Loading Setence Transformer...")

    embedder = SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2"
    )

    logger.info("Loading ML router...")

    router_model = joblib.load(
        MODELS_DIR / "fast_router_model.joblib"
    )

    return embedder, router_model

@asynccontextmanager
async def lifespan(app: FastAPI):

    manager.embedder, manager.router_model = await asyncio.to_thread(load_models)

    logger.info("Backend is ready!")

    yield

    logger.info("Shutting down backend...")

app = FastAPI(
    title = "Cost-Aware IT Support Router",
    lifespan=lifespan,
    version="1.0.0"
)

app.include_router(router)





