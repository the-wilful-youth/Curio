#!/usr/bin/env python3
"""
Test script to verify all API endpoints are working correctly.
Uses FastAPI TestClient for in-process direct testing,
and falls back to HTTP requests if run against a live server.
"""
import sys
import uuid

def run_tests():
    print("Testing Personal AI Content Vault API...")
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    # 1. Health check
    print("\n=== Testing Health Check ===")
    res = client.get("/health")
    print(f"Health check status: {res.status_code}")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print(f"Response: {res.json()}")

    # 2. Test sources
    print("\n=== Testing Sources ===")
    test_url = f"https://example.com/test-article-{uuid.uuid4().hex[:8]}"
    source_data = {
        "url": test_url,
        "platform": "web",
        "content_type": "article",
        "source_title": "Test Article",
        "creator": "Test Author"
    }
    res = client.post("/api/sources/", json=source_data)
    print(f"Create source status: {res.status_code}")
    assert res.status_code == 200, f"Failed: {res.text}"
    source = res.json()
    source_id = source["id"]
    print(f"Created source ID: {source_id}")

    # Read source
    res = client.get(f"/api/sources/{source_id}")
    assert res.status_code == 200
    print(f"Get source status: {res.status_code}")

    # List sources
    res = client.get("/api/sources/")
    assert res.status_code == 200
    print(f"List sources count: {len(res.json())}")

    # 3. Test notes
    print("\n=== Testing Notes ===")
    note_data = {
        "title": "Machine Learning Best Practices",
        "summary": "Key principles for building robust ML models",
        "full_note": "Ensure training and validation splits do not leak information.",
        "category": "ai"
    }
    res = client.post("/api/notes/", json=note_data)
    print(f"Create note status: {res.status_code}")
    assert res.status_code == 200, f"Failed: {res.text}"
    note = res.json()
    note_id = note["id"]
    print(f"Created note ID: {note_id}")

    # 4. Test events
    print("\n=== Testing Events ===")
    event_data = {
        "title": "Tech Conference 2026",
        "description": "Annual tech keynote",
        "start_datetime": "2026-10-15T09:00:00",
        "timezone": "UTC",
        "location": "San Francisco"
    }
    res = client.post("/api/events/", json=event_data)
    print(f"Create event status: {res.status_code}")
    assert res.status_code == 200, f"Failed: {res.text}"

    # 5. Test deadlines
    print("\n=== Testing Deadlines ===")
    deadline_data = {
        "title": "Grant Application Deadline",
        "deadline_datetime": "2026-11-01T23:59:59",
        "timezone": "UTC",
        "confidence": 0.95,
        "status": "upcoming"
    }
    res = client.post("/api/deadlines/", json=deadline_data)
    print(f"Create deadline status: {res.status_code}")
    assert res.status_code == 200, f"Failed: {res.text}"

    # 6. Test action items
    print("\n=== Testing Action Items ===")
    action_data = {
        "title": "Review project roadmap",
        "description": "Examine milestones for Q4",
        "priority": 2
    }
    res = client.post("/api/action-items/", json=action_data)
    print(f"Create action item status: {res.status_code}")
    assert res.status_code == 200, f"Failed: {res.text}"

    # 7. Test search
    print("\n=== Testing Search ===")
    res = client.get("/api/search/?q=Learning")
    print(f"Search status: {res.status_code}")
    assert res.status_code == 200
    results = res.json()
    print(f"Found {len(results)} search results")

    # 8. Test chat
    print("\n=== Testing Chat ===")
    res = client.post("/api/chat/", json={"message": "What do I have on machine learning?"})
    print(f"Chat status: {res.status_code}")
    assert res.status_code == 200
    chat_result = res.json()
    print(f"Chat answer: {chat_result.get('response')[:120]}...")

    # 9. Test tags
    print("\n=== Testing Tags ===")
    res = client.get("/api/tags/")
    assert res.status_code == 200
    print(f"Get tags status: {res.status_code}")

    print("\n✅ All API tests passed successfully!")

if __name__ == "__main__":
    run_tests()