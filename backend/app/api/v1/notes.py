from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models import User, Note
from ...schemas import NoteCreate, NoteResponse
from .sources import get_mock_user_id

router = APIRouter()

@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    note_data = note.dict() if hasattr(note, "dict") else note.model_dump()

    db_note = Note(
        **note_data,
        user_id=user_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/", response_model=List[NoteResponse])
def read_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    notes = db.query(Note).filter(Note.user_id == user_id).order_by(Note.created_at.desc()).offset(skip).limit(limit).all()
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
def read_note(
    note_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user_id
    ).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: str,
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    db_note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user_id
    ).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    note_data = note.dict() if hasattr(note, "dict") else note.model_dump()
    for key, value in note_data.items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
def delete_note(
    note_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user_id
    ).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}