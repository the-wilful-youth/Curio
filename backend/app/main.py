from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.main import api_router
from .config import settings

app = FastAPI(
    title="Personal AI Content Vault",
    description="A private, single-user system for capturing and understanding online content",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    from .database import init_db
    init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to Personal AI Content Vault"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}