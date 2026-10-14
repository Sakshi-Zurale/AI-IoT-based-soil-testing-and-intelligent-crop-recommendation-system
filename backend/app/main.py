from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

if __package__:
    from .config import settings
    from .database import Base, engine
    from .models import entities
    from .api.routes import router
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from app.config import settings
    from app.database import Base, engine
    from app.models import entities
    from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KrushiAI Module 1 API",
    description="AI-IoT Based Soil Testing and Crop Recommendation",
    version="1.0.0"
)

origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

@app.get("/")
def root():
    return {"name": "KrushiAI Module 1", "docs": "/docs"}
