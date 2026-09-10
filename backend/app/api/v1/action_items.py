from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ...models import User, ActionItem
from ...schemas import ActionItemCreate, ActionItemResponse
from .sources import get_mock_user_id

router = APIRouter()

@router.post("/", response_model=ActionItemResponse)
def create_action_item(
    action_item: ActionItemCreate,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    action_data = action_item.dict() if hasattr(action_item, "dict") else action_item.model_dump()

    db_action = ActionItem(
        **action_data,
        user_id=user_id
    )
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

@router.get("/", response_model=List[ActionItemResponse])
def read_action_items(
    completed: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    query = db.query(ActionItem).filter(ActionItem.user_id == user_id)
    if completed is not None:
        query = query.filter(ActionItem.completed == completed)

    action_items = query.order_by(ActionItem.priority.desc(), ActionItem.created_at.desc()).offset(skip).limit(limit).all()
    return action_items

@router.get("/{action_id}", response_model=ActionItemResponse)
def read_action_item(
    action_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    action = db.query(ActionItem).filter(
        ActionItem.id == action_id,
        ActionItem.user_id == user_id
    ).first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action item not found")
    return action

@router.put("/{action_id}", response_model=ActionItemResponse)
def update_action_item(
    action_id: str,
    action_item: ActionItemCreate,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    db_action = db.query(ActionItem).filter(
        ActionItem.id == action_id,
        ActionItem.user_id == user_id
    ).first()
    if db_action is None:
        raise HTTPException(status_code=404, detail="Action item not found")

    action_data = action_item.dict() if hasattr(action_item, "dict") else action_item.model_dump()
    for key, value in action_data.items():
        setattr(db_action, key, value)
    db.commit()
    db.refresh(db_action)
    return db_action

@router.delete("/{action_id}")
def delete_action_item(
    action_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    action = db.query(ActionItem).filter(
        ActionItem.id == action_id,
        ActionItem.user_id == user_id
    ).first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action item not found")

    db.delete(action)
    db.commit()
    return {"message": "Action item deleted successfully"}

@router.patch("/{action_id}/complete")
def complete_action_item(
    action_id: str,
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    action = db.query(ActionItem).filter(
        ActionItem.id == action_id,
        ActionItem.user_id == user_id
    ).first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action item not found")

    action.completed = True
    action.calendar_status = "completed"
    db.commit()
    return {"message": "Action item marked as complete"}