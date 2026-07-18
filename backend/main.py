from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.fusion_engine import fusion_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🌍 PlanetIQ Backend Started")
    yield
    print("🛑 PlanetIQ Backend Stopped")


app = FastAPI(
    title="PlanetIQ",
    version="1.0.0",
    description="AI-powered Ecosystem Intelligence Platform",
    lifespan=lifespan,
)

# ----------------------------
# CORS
# ----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "*",  # Remove "*" in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Request Model
# ----------------------------

class AnalyzeRequest(BaseModel):
    latitude: float
    longitude: float


# ----------------------------
# Routes
# ----------------------------

@app.get("/")
async def root():
    return {
        "project": "PlanetIQ",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "PlanetIQ Backend",
    }


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    return fusion_engine.analyze(
        request.latitude,
        request.longitude,
    )


@app.get("/info")
async def info():
    return {
        "name": "PlanetIQ",
        "version": "1.0.0",
        "features": [
            "Weather",
            "NASA FIRMS",
            "Fusion Engine",
            "Environmental Risk Assessment",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
