from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ...models import User, Deadline
from ...schemas import DeadlineCreate, DeadlineResponse
from .sources import get_mock_user_id

router = APIRouter()

@router.post("/", response_model=DeadlineResponse)
def create_deadline(
    deadline: DeadlineCreate,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    deadline_data = deadline.dict() if hasattr(deadline, "dict") else deadline.model_dump()

    db_deadline = Deadline(
        **deadline_data,
        user_id=user_id
    )
    db.add(db_deadline)
    db.commit()
    db.refresh(db_deadline)
    return db_deadline

@router.get("/", response_model=List[DeadlineResponse])
def read_deadlines(
    status: Optional[str] = Query(None),
    calendar_status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    query = db.query(Deadline).filter(Deadline.user_id == user_id)
    if status:
        query = query.filter(Deadline.status == status)
    if calendar_status:
        query = query.filter(Deadline.calendar_status == calendar_status)

    deadlines = query.order_by(Deadline.deadline_datetime.asc()).offset(skip).limit(limit).all()
    return deadlines

@router.get("/{deadline_id}", response_model=DeadlineResponse)
def read_deadline(
    deadline_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    deadline = db.query(Deadline).filter(
        Deadline.id == deadline_id,
        Deadline.user_id == user_id
    ).first()
    if deadline is None:
        raise HTTPException(status_code=404, detail="Deadline not found")
    return deadline

@router.put("/{deadline_id}", response_model=DeadlineResponse)
def update_deadline(
    deadline_id: str,
    deadline: DeadlineCreate,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    db_deadline = db.query(Deadline).filter(
        Deadline.id == deadline_id,
        Deadline.user_id == user_id
    ).first()
    if db_deadline is None:
        raise HTTPException(status_code=404, detail="Deadline not found")

    deadline_data = deadline.dict() if hasattr(deadline, "dict") else deadline.model_dump()
    for key, value in deadline_data.items():
        setattr(db_deadline, key, value)
    db.commit()
    db.refresh(db_deadline)
    return db_deadline

@router.delete("/{deadline_id}")
def delete_deadline(
    deadline_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    deadline = db.query(Deadline).filter(
        Deadline.id == deadline_id,
        Deadline.user_id == user_id
    ).first()
    if deadline is None:
        raise HTTPException(status_code=404, detail="Deadline not found")

    db.delete(deadline)
    db.commit()
    return {"message": "Deadline deleted successfully"}

@router.post("/{deadline_id}/calendar")
def create_calendar_deadline(
    deadline_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    deadline = db.query(Deadline).filter(
        Deadline.id == deadline_id,
        Deadline.user_id == user_id
    ).first()
    if deadline is None:
        raise HTTPException(status_code=404, detail="Deadline not found")

    deadline.calendar_status = "scheduled"
    db.commit()
    return {"message": "Calendar deadline scheduled", "deadline_id": deadline_id}