from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import hashlib

from ...database import get_db, SessionLocal
from ...models import User, Source, ContentItem
from ...schemas import SourceCreate, SourceResponse, ContentItemCreate, ContentItemResponse
from ...config import settings

router = APIRouter()

def get_mock_user_id(db: Session = None) -> str:
    mock_id = "00000000-0000-0000-0000-000000000001"
    if db is not None:
        user = db.query(User).filter(User.id == mock_id).first()
        if not user:
            user = User(
                id=mock_id,
                email="user@curio.local",
                name="Vault User",
                timezone="UTC"
            )
            db.add(user)
            db.commit()
    return mock_id

def generate_content_hash(url: str) -> str:
    """Generate a hash for deduplication"""
    return hashlib.md5(url.encode()).hexdigest()

@router.post("/", response_model=SourceResponse)
def create_source(
    source: SourceCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)

    # Check if URL already exists (deduplication)
    content_hash = generate_content_hash(str(source.url))
    existing_source = db.query(Source).filter(
        Source.user_id == user_id,
        Source.content_hash == content_hash
    ).first()

    if existing_source:
        raise HTTPException(
            status_code=400,
            detail="This URL has already been processed"
        )

    # Auto-detect platform if web
    platform = source.platform
    url_str = str(source.url).lower()
    if "youtube.com" in url_str or "youtu.be" in url_str:
        platform = "youtube"

    # Create source record
    source_data = source.dict() if hasattr(source, "dict") else source.model_dump()
    source_data["url"] = str(source_data["url"])
    source_data["platform"] = platform

    db_source = Source(
        **source_data,
        user_id=user_id,
        content_hash=content_hash,
        status="queued"
    )
    db.add(db_source)
    db.commit()
    db.refresh(db_source)

    # Create content item record
    db_content_item = ContentItem(
        source_id=db_source.id
    )
    db.add(db_content_item)
    db.commit()
    db.refresh(db_content_item)

    # Queue background task for extraction & analysis
    background_tasks.add_task(process_content, db_source.id)

    return db_source

@router.get("/", response_model=List[SourceResponse])
def read_sources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    sources = db.query(Source).filter(Source.user_id == user_id).order_by(Source.created_at.desc()).offset(skip).limit(limit).all()
    return sources

@router.get("/{source_id}", response_model=SourceResponse)
def read_source(
    source_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    source = db.query(Source).filter(
        Source.id == source_id,
        Source.user_id == user_id
    ).first()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

@router.delete("/{source_id}")
def delete_source(
    source_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    source = db.query(Source).filter(
        Source.id == source_id,
        Source.user_id == user_id
    ).first()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")

    db.delete(source)
    db.commit()
    return {"message": "Source deleted successfully"}

def process_content(source_id: str):
    """Background task to extract and analyze content"""
    try:
        from ...workers.pipeline import run_extraction_and_analysis
        run_extraction_and_analysis(source_id)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error processing source {source_id}: {e}")
        db = SessionLocal()
        try:
            source = db.query(Source).filter(Source.id == source_id).first()
            if source:
                source.status = "failed"
                db.commit()
        finally:
            db.close()