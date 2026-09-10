import logging
from datetime import datetime, timezone
from ..database import SessionLocal
from ..models import Source, ContentItem, Note, ExtractedFact, Event, Deadline, ActionItem, Image
from ..extractors.factory import ExtractorFactory
from ..ai.service import AIService

logger = logging.getLogger(__name__)

def run_extraction_and_analysis(source_id: str):
    """
    Unified extraction and processing pipeline.
    Usable by both FastAPI BackgroundTasks and Celery workers.
    """
    db = SessionLocal()
    try:
        source = db.query(Source).filter(Source.id == source_id).first()
        if not source:
            logger.error(f"Source {source_id} not found")
            return

        source.status = "processing"
        db.commit()

        logger.info(f"Extracting content for source {source_id}: {source.url}")
        extractor_factory = ExtractorFactory()
        extracted = extractor_factory.extract(source.url)

        if extracted.get('title') and not source.source_title:
            source.source_title = extracted['title']
        if extracted.get('creator') and not source.creator:
            source.creator = extracted['creator']

        # Update ContentItem
        content_item = db.query(ContentItem).filter(ContentItem.source_id == source_id).first()
        if not content_item:
            content_item = ContentItem(source_id=source_id)
            db.add(content_item)
            db.flush()

        content_item.raw_text = extracted.get('text', '')
        content_item.caption = extracted.get('caption', '')
        content_item.transcript = extracted.get('transcript', '')
        content_item.description = extracted.get('caption', '')

        # Store extracted images
        if extracted.get('images'):
            for img_info in extracted['images'][:5]:
                if img_info.get('url'):
                    existing_img = db.query(Image).filter(
                        Image.content_item_id == content_item.id,
                        Image.original_url == img_info['url']
                    ).first()
                    if not existing_img:
                        db_img = Image(
                            content_item_id=content_item.id,
                            source_id=source_id,
                            storage_path=img_info['url'],
                            original_url=img_info['url'],
                            image_type=img_info.get('type', 'unknown')
                        )
                        db.add(db_img)

        # Generate Note from extracted content
        title = extracted.get('title') or f"Saved from {source.platform.capitalize()}"
        summary = extracted.get('caption') or (extracted.get('text', '')[:280] if extracted.get('text') else "")
        full_note = extracted.get('text', '')

        # Check if note exists
        existing_note = db.query(Note).filter(Note.source_id == source_id).first()
        if not existing_note:
            note = Note(
                source_id=source_id,
                content_item_id=content_item.id,
                user_id=source.user_id,
                title=title,
                summary=summary,
                full_note=full_note,
                category=source.platform or "general"
            )
            db.add(note)
        else:
            existing_note.title = title
            existing_note.summary = summary
            existing_note.full_note = full_note

        source.status = "completed"
        db.commit()
        logger.info(f"Successfully processed source {source_id}")

    except Exception as e:
        logger.error(f"Failed to process source {source_id}: {e}", exc_info=True)
        try:
            source = db.query(Source).filter(Source.id == source_id).first()
            if source:
                source.status = "failed"
                db.commit()
        except Exception:
            pass
    finally:
        db.close()
