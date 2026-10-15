from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Pre-Trip Decision Support System",
    version=settings.VERSION
)

# Allow CORS for React Frontend (Tanvi's UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend engine is running smoothly!"}
