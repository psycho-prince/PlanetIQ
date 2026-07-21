from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers.health import router as health_router
from backend.app.routers.analyze import router as analyze_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🌍 PlanetIQ starting...")
    yield
    print("🛑 PlanetIQ shutting down...")


app = FastAPI(
    title="PlanetIQ",
    description="AI-powered environmental intelligence platform",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, tags=["Health"])
app.include_router(analyze_router, tags=["Analysis"])


@app.get("/", tags=["Root"])
async def root():
    return {
        "project": "PlanetIQ",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
    }
