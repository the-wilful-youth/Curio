from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models import User, Note
from ...schemas import NoteResponse
from .sources import get_mock_user_id

router = APIRouter()

@router.get("/", response_model=List[NoteResponse])
def search_content(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)

    search_term = f"%{q.strip()}%"
    notes = db.query(Note).filter(
        Note.user_id == user_id,
        (Note.title.ilike(search_term)) |
        (Note.summary.ilike(search_term)) |
        (Note.full_note.ilike(search_term))
    ).order_by(Note.created_at.desc()).limit(30).all()

    return notes