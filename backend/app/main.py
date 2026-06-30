from fastapi import FastAPI
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from ml_pipeline.config import MODELS_DIR
from backend.app.model_manager import manager
from backend.app.api.routes import router
import joblib

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("Loading Setence Transformer...")

    manager.embedder = SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2"
    )

    print("Loading ML router...")

    manager.router_model = joblib.load(
        MODELS_DIR / "fast_router_model.joblib"
    )

    print("Backend is ready!")

    yield

    print("Shutting down backend...")

app = FastAPI(
    title = "Cost-Aware IT Support Router",
    lifespan=lifespan,
    version="1.0.0"
)

app.include_router(router)





