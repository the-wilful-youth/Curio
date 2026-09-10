from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import inspect
from ...database import get_db
from ...models import User, Note, ExtractedFact, Event, Deadline, ActionItem, ContentItem, Source
from ...ai.service import AIService
from .sources import get_mock_user_id

router = APIRouter()

# Initialize AI service
ai_service = AIService()

@router.post("/", response_model=Dict[str, Any])
async def chat_with_knowledge(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    user_id = get_mock_user_id(db)
    user_message = request.get('message', '').strip()

    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    try:
        # Retrieve relevant content from the knowledge base
        relevant_content = retrieve_relevant_content(db, user_id, user_message)

        # Prepare context for AI
        context = prepare_context(relevant_content)

        answer = None
        # Attempt AI analysis if provider is configured
        try:
            prompt_content = (
                f"Based on the following information from the user's personal knowledge base:\n\n"
                f"{context}\n\n"
                f"User question: {user_message}\n\n"
                f"Provide a concise, helpful answer based on the information provided above."
            )
            analysis_call = ai_service.llm_provider.analyze(
                content=prompt_content,
                prompt_type="content_analysis"
            )
            if inspect.iscoroutine(analysis_call):
                response = await analysis_call
            else:
                response = analysis_call

            if isinstance(response, dict):
                answer = response.get('summary') or response.get('answer') or response.get('response')
        except Exception:
            answer = None

        # Fallback if no LLM provider configured or error
        if not answer or "error" in str(answer).lower():
            if relevant_content:
                top_items = relevant_content[:3]
                snippets = []
                for item in top_items:
                    snippets.append(f"• **{item['title']}**: {item['summary']}")
                answer = f"Found relevant information in your vault:\n\n" + "\n".join(snippets)
            else:
                answer = "I searched your vault but didn't find any notes, events, or deadlines matching your query. Try saving relevant content first!"

        return {
            "response": answer,
            "sources": [item.get('title', 'Unknown') for item in relevant_content[:3]]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

def retrieve_relevant_content(db: Session, user_id: str, query: str) -> List[Dict[str, Any]]:
    relevant_items = []
    search_term = f"%{query.strip()}%"

    # Search notes
    notes = db.query(Note).filter(
        Note.user_id == user_id,
        (Note.title.ilike(search_term)) |
        (Note.summary.ilike(search_term)) |
        (Note.full_note.ilike(search_term))
    ).limit(10).all()

    for note in notes:
        relevant_items.append({
            "id": note.id,
            "type": "note",
            "title": note.title,
            "summary": note.summary or (note.full_note[:150] if note.full_note else ""),
            "content": note.full_note or ""
        })

    # Search extracted facts via ContentItem -> Source
    facts = db.query(ExtractedFact)\
        .join(ContentItem, ExtractedFact.content_item_id == ContentItem.id)\
        .join(Source, ContentItem.source_id == Source.id)\
        .filter(
            Source.user_id == user_id,
            ExtractedFact.value.ilike(search_term)
        ).limit(10).all()

    for fact in facts:
        relevant_items.append({
            "id": fact.id,
            "type": "fact",
            "title": f"{fact.fact_type}: {fact.value}",
            "summary": fact.value,
            "content": f"Fact type: {fact.fact_type}, Value: {fact.value}"
        })

    # Search events
    events = db.query(Event).filter(
        Event.user_id == user_id,
        (Event.title.ilike(search_term)) |
        (Event.description.ilike(search_term))
    ).limit(5).all()

    for event in events:
        start_str = event.start_datetime.strftime("%Y-%m-%d %H:%M") if event.start_datetime else ""
        relevant_items.append({
            "id": event.id,
            "type": "event",
            "title": event.title,
            "summary": f"Event on {start_str}: {event.description or ''}",
            "content": f"Event: {event.title} on {start_str}"
        })

    # Search deadlines
    deadlines = db.query(Deadline).filter(
        Deadline.user_id == user_id,
        (Deadline.title.ilike(search_term))
    ).limit(5).all()

    for deadline in deadlines:
        dl_str = deadline.deadline_datetime.strftime("%Y-%m-%d %H:%M") if deadline.deadline_datetime else ""
        relevant_items.append({
            "id": deadline.id,
            "type": "deadline",
            "title": deadline.title,
            "summary": f"Deadline on {dl_str}",
            "content": f"Deadline: {deadline.title} due {dl_str}"
        })

    return relevant_items

def prepare_context(relevant_items: List[Dict[str, Any]]) -> str:
    if not relevant_items:
        return "No relevant information found in your knowledge base."

    context_parts = []
    for i, item in enumerate(relevant_items[:5], 1):
        context_parts.append(
            f"{i}. [{item['type'].upper()}] {item['title']}\n"
            f"   Summary: {item['summary']}\n"
            f"   Details: {item['content'][:200]}{'...' if len(item['content']) > 200 else ''}\n"
        )

    return "\n".join(context_parts)