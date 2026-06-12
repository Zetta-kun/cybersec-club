from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from .core.config import settings
from .core.database import init_db
from .api.v1.router import api_router
import logging

logging.basicConfig(level=settings.LOG_LEVEL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 {settings.APP_NAME} v{settings.VERSION} starting...")
    await init_db()
    yield
    logger.info("👋 Server shutting down...")

app = FastAPI(title=settings.APP_NAME, description="Kiber Təhlükəsizlik Klubu - Professional CTF Platform", version=settings.VERSION, docs_url="/api/docs" if settings.DEBUG else None, redoc_url="/api/redoc" if settings.DEBUG else None, lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "version": settings.VERSION, "status": "operational"}

@app.get("/health")
async def health():
    from datetime import datetime
    return {"status": "healthy", "version": settings.VERSION, "timestamp": datetime.utcnow().isoformat()}
