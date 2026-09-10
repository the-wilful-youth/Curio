from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ...database import get_db
from ...models import User, Tag, Note, ContentTag
from ...schemas import TagResponse
from .sources import get_mock_user_id

router = APIRouter()

@router.get("/", response_model=List[TagResponse])
def get_tags(
    db: Session = Depends(get_db)
):
    tags = db.query(Tag).order_by(Tag.name).all()
    return tags

@router.get("/popular", response_model=List[TagResponse])
def get_popular_tags(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)

    popular_tags = db.query(Tag, func.count(ContentTag.id).label('usage_count'))\
        .join(ContentTag, Tag.id == ContentTag.tag_id)\
        .join(Note, ContentTag.content_id == Note.id)\
        .filter(Note.user_id == user_id)\
        .group_by(Tag.id)\
        .order_by(func.count(ContentTag.id).desc())\
        .limit(limit)\
        .all()

    tags = [tag for tag, count in popular_tags]
    if not tags:
        tags = db.query(Tag).order_by(Tag.name).limit(limit).all()
    return tags