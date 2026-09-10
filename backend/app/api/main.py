from fastapi import APIRouter
from .v1 import sources, notes, events, deadlines, action_items, search, chat, tags

api_router = APIRouter()

api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(deadlines.router, prefix="/deadlines", tags=["deadlines"])
api_router.include_router(action_items.router, prefix="/action-items", tags=["action-items"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])

# Additional routers will be added here as we implement them
# api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])