from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    timezone = Column(String, default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sources = relationship("Source", back_populates="user")
    notes = relationship("Note", back_populates="user")
    events = relationship("Event", back_populates="user")
    deadlines = relationship("Deadline", back_populates="user")
    action_items = relationship("ActionItem", back_populates="user")

class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    url = Column(Text, nullable=False)
    platform = Column(String, nullable=False)  # instagram, youtube, linkedin, x, web, pdf, other
    content_type = Column(String, nullable=False)  # post, reel, video, shorts, article, pdf, etc.
    source_title = Column(String)
    creator = Column(String)
    source_created_at = Column(DateTime)
    shared_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="queued")  # queued, processing, completed, partial, failed
    content_hash = Column(String)  # For deduplication
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="sources")
    content_item = relationship("ContentItem", back_populates="source", uselist=False)
    notes = relationship("Note", back_populates="source")
    images = relationship("Image", back_populates="source")
    events = relationship("Event", back_populates="source")
    deadlines = relationship("Deadline", back_populates="source")
    action_items = relationship("ActionItem", back_populates="source")

class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(String, primary_key=True, default=generate_uuid)
    source_id = Column(String, ForeignKey("sources.id"), nullable=False)
    raw_text = Column(Text)
    caption = Column(Text)
    transcript = Column(Text)
    description = Column(Text)
    language = Column(String)
    processing_version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source = relationship("Source", back_populates="content_item")
    note = relationship("Note", back_populates="content_item", uselist=False)
    images = relationship("Image", back_populates="content_item")
    extracted_facts = relationship("ExtractedFact", back_populates="content_item")
    embeddings = relationship("Embedding", back_populates="content_item")
    events = relationship("Event", back_populates="content_item")
    deadlines = relationship("Deadline", back_populates="content_item")
    action_items = relationship("ActionItem", back_populates="content_item")

class Image(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True, default=generate_uuid)
    content_item_id = Column(String, ForeignKey("content_items.id"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id"), nullable=False)
    storage_path = Column(String, nullable=False)
    original_url = Column(String)
    image_type = Column(String)  # poster, screenshot, carousel_slide, diagram, photo, decorative, unknown
    ocr_text = Column(Text)
    vision_description = Column(Text)
    importance_score = Column(Float, default=0.0)
    is_important = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content_item = relationship("ContentItem", back_populates="images")
    source = relationship("Source", back_populates="images")

class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, default=generate_uuid)
    content_item_id = Column(String, ForeignKey("content_items.id"), nullable=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    full_note = Column(Text)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content_item = relationship("ContentItem", back_populates="note")
    source = relationship("Source", back_populates="notes")
    user = relationship("User", back_populates="notes")
    tags = relationship("Tag", secondary="content_tags", back_populates="notes")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    notes = relationship("Note", secondary="content_tags", back_populates="tags")

class ContentTag(Base):
    __tablename__ = "content_tags"

    id = Column(String, primary_key=True, default=generate_uuid)
    content_id = Column(String, ForeignKey("notes.id"), nullable=False)
    tag_id = Column(String, ForeignKey("tags.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExtractedFact(Base):
    __tablename__ = "extracted_facts"

    id = Column(String, primary_key=True, default=generate_uuid)
    content_item_id = Column(String, ForeignKey("content_items.id"), nullable=True)
    fact_type = Column(String, nullable=False)  # event_date, deadline, location, fee, eligibility, contact, registration_url, prize, organizer
    value = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    source_reference = Column(String)  # Which image, transcript section, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    content_item = relationship("ContentItem", back_populates="extracted_facts")

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=generate_uuid)
    content_item_id = Column(String, ForeignKey("content_items.id"), nullable=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime)
    timezone = Column(String, nullable=False)
    location = Column(String)
    calendar_status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    external_calendar_id = Column(String)  # Google Calendar event ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content_item = relationship("ContentItem", back_populates="events")
    source = relationship("Source", back_populates="events")
    user = relationship("User", back_populates="events")

class Deadline(Base):
    __tablename__ = "deadlines"

    id = Column(String, primary_key=True, default=generate_uuid)
    content_item_id = Column(String, ForeignKey("content_items.id"), nullable=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    deadline_datetime = Column(DateTime, nullable=False)
    timezone = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    status = Column(String, default="upcoming")  # upcoming, completed, expired, cancelled, unknown
    calendar_status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    external_calendar_id = Column(String)  # Google Calendar event ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content_item = relationship("ContentItem", back_populates="deadlines")
    source = relationship("Source", back_populates="deadlines")
    user = relationship("User", back_populates="deadlines")

class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(String, primary_key=True, default=generate_uuid)
    content_item_id = Column(String, ForeignKey("content_items.id"), nullable=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    due_datetime = Column(DateTime)
    priority = Column(Integer, default=1)  # 1=low, 2=medium, 3=high
    completed = Column(Boolean, default=False)
    calendar_status = Column(String, default="unscheduled")  # unscheduled, scheduled, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content_item = relationship("ContentItem", back_populates="action_items")
    source = relationship("Source", back_populates="action_items")
    user = relationship("User", back_populates="action_items")

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(String, primary_key=True, default=generate_uuid)
    content_item_id = Column(String, ForeignKey("content_items.id"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    # Using pgvector - in practice this would be a Vector type, but we'll store as JSON for simplicity
    # In production, you'd use: embedding = Column(Vector(1536)) for OpenAI embeddings
    embedding = Column(JSON)  # Temporary - replace with actual vector type when using pgvector
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    content_item = relationship("ContentItem", back_populates="embeddings")