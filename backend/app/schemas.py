from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class AppBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# Tag schemas
class TagBase(AppBaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: str
    created_at: datetime

Tag = TagResponse

# Source schemas
class SourceBase(AppBaseModel):
    url: str
    platform: str
    content_type: str
    source_title: Optional[str] = None
    creator: Optional[str] = None
    source_created_at: Optional[datetime] = None

class SourceCreate(SourceBase):
    pass

class SourceResponse(SourceBase):
    id: str
    user_id: str
    shared_at: datetime
    status: str
    content_hash: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Content item schemas
class ContentItemBase(AppBaseModel):
    raw_text: Optional[str] = None
    caption: Optional[str] = None
    transcript: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None

class ContentItemCreate(ContentItemBase):
    pass

class ContentItemResponse(ContentItemBase):
    id: str
    source_id: str
    processing_version: int
    created_at: datetime
    updated_at: datetime

# Note schemas
class NoteBase(AppBaseModel):
    title: str
    summary: Optional[str] = None
    full_note: Optional[str] = None
    category: Optional[str] = None
    content_item_id: Optional[str] = None
    source_id: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    tags: Optional[List[TagResponse]] = []

# Image schemas
class ImageBase(AppBaseModel):
    storage_path: str
    original_url: Optional[str] = None
    image_type: Optional[str] = None
    ocr_text: Optional[str] = None
    vision_description: Optional[str] = None
    importance_score: Optional[float] = None
    is_important: Optional[bool] = None

class ImageCreate(ImageBase):
    pass

class ImageResponse(ImageBase):
    id: str
    content_item_id: Optional[str] = None
    source_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Extracted fact schemas
class ExtractedFactBase(AppBaseModel):
    fact_type: str
    value: str
    confidence: float
    source_reference: Optional[str] = None

class ExtractedFactCreate(ExtractedFactBase):
    content_item_id: Optional[str] = None

class ExtractedFactResponse(ExtractedFactBase):
    id: str
    content_item_id: Optional[str] = None
    created_at: datetime

# Event schemas
class EventBase(AppBaseModel):
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: Optional[datetime] = None
    timezone: str = "UTC"
    location: Optional[str] = None
    content_item_id: Optional[str] = None
    source_id: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: str
    user_id: str
    calendar_status: str = "scheduled"
    external_calendar_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Deadline schemas
class DeadlineBase(AppBaseModel):
    title: str
    deadline_datetime: datetime
    timezone: str = "UTC"
    confidence: float = 1.0
    status: Optional[str] = "upcoming"
    content_item_id: Optional[str] = None
    source_id: Optional[str] = None

class DeadlineCreate(DeadlineBase):
    pass

class DeadlineResponse(DeadlineBase):
    id: str
    user_id: str
    calendar_status: str = "scheduled"
    external_calendar_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Action item schemas
class ActionItemBase(AppBaseModel):
    title: str
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: Optional[int] = 1
    completed: Optional[bool] = False
    content_item_id: Optional[str] = None
    source_id: Optional[str] = None

class ActionItemCreate(ActionItemBase):
    pass

class ActionItemResponse(ActionItemBase):
    id: str
    user_id: str
    calendar_status: str = "unscheduled"
    created_at: datetime
    updated_at: datetime

# API response schemas
class APIResponse(AppBaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class PaginatedResponse(AppBaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int