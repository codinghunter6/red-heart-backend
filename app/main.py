import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config import settings
from app.core.db import Base, engine

# ── Logging setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("red_heart")
# ──────────────────────────────────────────────────────────────────────────────


def create_tables():
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up — creating database tables if needed")
    create_tables()
    logger.info("Startup complete")
    yield
    logger.info("Shutting down")


app = FastAPI(title="Red Heart API", lifespan=lifespan)

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    req_id = uuid.uuid4().hex[:8]
    start = time.perf_counter()
    logger.info("[%s] → %s %s", req_id, request.method, request.url.path)

    response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "[%s] ← %s %s  %d  %.1f ms",
        req_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


app.include_router(api_router)


@app.get("/")
def root():
    logger.debug("root endpoint called")
    return {"message": "Red Heart API", "status": "ok"}


@app.get("/health")
def health():
    logger.debug("health check called")
    return {"status": "healthy"}
