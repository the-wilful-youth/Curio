from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ...models import User, Event
from ...schemas import EventCreate, EventResponse
from .sources import get_mock_user_id

router = APIRouter()

@router.post("/", response_model=EventResponse)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    event_data = event.dict() if hasattr(event, "dict") else event.model_dump()

    db_event = Event(
        **event_data,
        user_id=user_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=List[EventResponse])
def read_events(
    calendar_status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    query = db.query(Event).filter(Event.user_id == user_id)
    if calendar_status:
        query = query.filter(Event.calendar_status == calendar_status)
    events = query.order_by(Event.start_datetime.asc()).offset(skip).limit(limit).all()
    return events

@router.get("/{event_id}", response_model=EventResponse)
def read_event(
    event_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.user_id == user_id
    ).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: str,
    event: EventCreate,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    db_event = db.query(Event).filter(
        Event.id == event_id,
        Event.user_id == user_id
    ).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event_data = event.dict() if hasattr(event, "dict") else event.model_dump()
    for key, value in event_data.items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
def delete_event(
    event_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.user_id == user_id
    ).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}

@router.post("/{event_id}/calendar")
def create_calendar_event(
    event_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.user_id == user_id
    ).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event.calendar_status = "scheduled"
    db.commit()
    return {"message": "Calendar event scheduled", "event_id": event_id}