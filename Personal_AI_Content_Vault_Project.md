# Personal AI Content Intelligence & Reminder System

## 1. Project Overview

### Working name
**Personal AI Content Vault**

### One-line idea

A private, single-user system where I can share links from Instagram, YouTube, websites, event pages, posts, reels, shorts, PDFs, etc. The system automatically extracts and understands the content, stores a structured note, preserves useful images, detects dates/deadlines/action items, and—after confirmation—creates calendar events and reminders.

### Core workflow

```text
Share a link
    ↓
System receives URL
    ↓
Identify platform/content type
    ↓
Extract available text, media, metadata and transcript
    ↓
OCR useful images
    ↓
Vision analysis of images
    ↓
LLM analyzes all gathered information
    ↓
Extract structured facts
    ↓
Create a clean permanent note
    ↓
Detect:
  - dates
  - deadlines
  - events
  - tasks
  - requirements
  - useful links
    ↓
Show review screen
    ↓
User confirms calendar/reminder actions
    ↓
Store everything
    ↓
Search / filter / ask AI questions later
```

---

# 2. Why Build This?

Useful information is increasingly encountered as short-lived content:

- Instagram Reels
- Instagram carousels
- YouTube Shorts
- YouTube videos
- LinkedIn posts
- X posts
- Event announcements
- Posters
- Screenshots
- Articles
- PDFs

The problem is that saving a URL does not preserve the useful information.

For example, an event Reel may contain:

- event name in the caption
- deadline in the video
- eligibility in an image
- registration link in the profile/bio
- venue in a poster
- prize details on another slide

The system should combine all of these into one reliable record.

---

# 3. Product Goals

## Must have

1. Share a URL.
2. Automatically identify the source.
3. Extract available content.
4. Extract captions/text.
5. Extract video transcript where possible.
6. Extract important images.
7. OCR images.
8. Analyze images with a vision model.
9. Generate a useful summary.
10. Extract structured information.
11. Detect deadlines.
12. Detect event dates.
13. Detect action items.
14. Store the original URL.
15. Store source media where legally/technically appropriate.
16. Allow manual correction.
17. Search all saved information.
18. Integrate with Google Calendar.
19. Create reminders after user confirmation.
20. Keep the system private and single-user.

## Nice to have later

- Browser extension.
- Mobile share sheet.
- WhatsApp/Telegram forwarding.
- Email forwarding.
- AI chat over saved knowledge.
- Automatic deadline monitoring.
- Duplicate detection.
- Weekly digest.
- Semantic search.
- Automatic tagging.
- Event status tracking.
- Export to Markdown/PDF/JSON.
- Local/self-hosted deployment.

---

# 4. Important Design Principle

Do **not** build this as a simple "AI summarizer".

Build it as:

> **Content ingestion + information extraction + personal knowledge management + action management.**

The summary is only one output.

The important output is the structured knowledge.

---

# 5. Example

Suppose I share:

```text
https://instagram.com/reel/abc123
```

The Reel contains:

> "Join our AI Hackathon..."

The video contains a poster showing:

```text
AI Hackathon 2026
25-27 September
Registration closes: 18 September
Fee: ₹299
Venue: IIT Delhi
Eligibility: College students
```

The system should create:

```text
Title:
AI Hackathon 2026

Category:
Hackathon

Summary:
Three-day AI hackathon for college students.

Important information:
- Date: 25–27 September 2026
- Registration deadline: 18 September 2026
- Fee: ₹299
- Venue: IIT Delhi
- Eligibility: College students

Actions:
- Register
- Prepare required materials

Calendar:
Event detected

Reminder:
Registration deadline detected

Images:
Poster saved as important image

Source:
Original Instagram URL
```

---

# 6. System Architecture

```text
                         ┌──────────────────┐
                         │      USER        │
                         └────────┬─────────┘
                                  │
                         Share URL / Upload
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  API / Backend   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Ingestion Queue  │
                         └────────┬─────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 ▼                ▼                ▼
          ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
          │ Instagram   │  │ YouTube     │  │ Web/PDF     │
          │ Extractor   │  │ Extractor   │  │ Extractor   │
          └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
                 │                │                │
                 └────────────────┼────────────────┘
                                  ▼
                         ┌──────────────────┐
                         │ Raw Content      │
                         │ Normalization     │
                         └────────┬─────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 ▼                ▼                ▼
             Text/HTML       Transcript        Images
                 │                │                │
                 │                │                ▼
                 │                │         ┌─────────────┐
                 │                │         │ OCR + Vision│
                 │                │         └──────┬──────┘
                 │                │                │
                 └────────────────┼────────────────┘
                                  ▼
                         ┌──────────────────┐
                         │ AI Analysis      │
                         │ / LLM Pipeline   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Structured Data  │
                         └────────┬─────────┘
                                  │
             ┌────────────────────┼─────────────────────┐
             ▼                    ▼                     ▼
        ┌──────────┐        ┌────────────┐        ┌──────────┐
        │ Database │        │ Calendar   │        │ Storage  │
        │           │        │ Integration│        │ Images   │
        └─────┬────┘        └────────────┘        └──────────┘
              │
              ▼
        ┌──────────────────┐
        │ Search / AI Chat │
        └──────────────────┘
```

---

# 7. Recommended Tech Stack

## Frontend

### Recommended

- Next.js
- React
- TypeScript
- Tailwind CSS

Why:

- fast development
- responsive UI
- easy API integration
- easy authentication if needed later
- good ecosystem

The interface should work well on desktop and mobile.

---

# 8. Backend

### Recommended

**Python + FastAPI**

Reasons:

- excellent AI ecosystem
- easy OCR integration
- easy media processing
- easy API development
- easy background processing
- easy integration with LLM providers

Suggested structure:

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── extractors/
│   ├── ai/
│   ├── calendar/
│   ├── storage/
│   ├── search/
│   └── workers/
└── tests/
```

---

# 9. Database

## PostgreSQL

Use PostgreSQL as the primary database.

Add:

- `pgvector` for semantic search
- normal relational tables for structured information

Avoid using a separate vector database during the MVP.

---

# 10. Storage

Images, videos, PDFs and other files should not be stored directly inside PostgreSQL.

Use object storage.

Options:

- local filesystem during development
- S3-compatible storage later
- Cloudflare R2
- AWS S3
- Supabase Storage

Recommended development approach:

```text
Local development:
PostgreSQL + local media directory

Production:
PostgreSQL + object storage
```

---

# 11. Single-User Architecture

Because only I will use the system, do not over-engineer multi-tenancy.

There can still be a `users` table, but the initial system can operate with one account.

Recommended:

```text
users
  id
  email
  name
  timezone
  created_at
```

Everything else references the user.

This makes it possible to add authentication later without redesigning the database.

---

# 12. Database Design

## users

```text
id
email
name
timezone
created_at
updated_at
```

## sources

Stores original shared URLs.

```text
id
user_id
url
platform
content_type
source_title
creator
source_created_at
shared_at
status
content_hash
created_at
updated_at
```

Possible `platform` values:

```text
instagram
youtube
linkedin
x
web
pdf
other
```

Possible `status` values:

```text
queued
processing
completed
partial
failed
```

---

# 13. content_items

Represents the normalized content.

```text
id
source_id
raw_text
caption
transcript
description
language
processing_version
created_at
updated_at
```

---

# 14. images

```text
id
content_item_id
storage_path
original_url
image_type
ocr_text
vision_description
importance_score
is_important
created_at
```

`image_type` examples:

```text
poster
screenshot
carousel_slide
diagram
photo
decorative
unknown
```

---

# 15. notes

The final human-readable representation.

```text
id
content_item_id
title
summary
full_note
category
created_at
updated_at
```

---

# 16. tags

```text
id
name
```

## content_tags

```text
content_id
tag_id
```

Examples:

```text
hackathon
internship
event
cybersecurity
AI
college
competition
learning
```

---

# 17. extracted_facts

Store important structured information separately.

```text
id
content_item_id
fact_type
value
confidence
source_reference
created_at
```

Examples:

```text
event_date
deadline
location
fee
eligibility
contact
registration_url
prize
organizer
```

---

# 18. events

```text
id
content_item_id
title
description
start_datetime
end_datetime
timezone
location
calendar_status
external_calendar_id
created_at
```

---

# 19. deadlines

```text
id
content_item_id
title
deadline_datetime
timezone
confidence
status
calendar_status
external_calendar_id
created_at
```

Possible status:

```text
upcoming
completed
expired
cancelled
unknown
```

---

# 20. action_items

```text
id
content_item_id
title
description
due_datetime
priority
completed
calendar_status
created_at
updated_at
```

Example:

```text
Download application form
Fill application
Submit application
```

---

# 21. embeddings

Can either be stored directly on the content table or separately.

```text
id
content_item_id
chunk_text
embedding
created_at
```

Use pgvector.

---

# 22. AI Processing Pipeline

The processing pipeline should be modular.

```text
URL
 ↓
Platform detection
 ↓
Extractor
 ↓
Content normalization
 ↓
Media extraction
 ↓
OCR
 ↓
Vision
 ↓
Transcript
 ↓
LLM structured extraction
 ↓
Validation
 ↓
Note generation
 ↓
Save
```

Do not send everything to the LLM blindly.

First collect and normalize information.

---

# 23. Step 1 — URL Detection

The backend should determine:

```text
Instagram URL
YouTube URL
normal website
PDF
unknown
```

Example:

```text
instagram.com/reel/...
youtube.com/shorts/...
youtube.com/watch/...
```

Use dedicated extractors.

---

# 24. Step 2 — Content Extraction

Create a common extractor interface.

```python
class ContentExtractor:
    def can_handle(self, url):
        ...

    def extract(self, url):
        ...
```

Implement:

```text
InstagramExtractor
YouTubeExtractor
WebExtractor
PDFExtractor
```

Every extractor should return normalized data.

Example:

```json
{
  "title": "...",
  "caption": "...",
  "text": "...",
  "transcript": "...",
  "images": [],
  "video": "...",
  "creator": "...",
  "published_at": "...",
  "source_url": "..."
}
```

---

# 25. Important Platform Constraint

Do not assume every platform allows unrestricted scraping or downloading.

Instagram and other platforms can have:

- API restrictions
- authentication requirements
- private content
- anti-bot systems
- rate limits
- changing page structures
- copyright restrictions

Therefore the system needs fallback behavior.

Example:

```text
Automatic extraction
       ↓
If successful → process normally

If incomplete → process available information

If unavailable →
ask user to upload:
- video
- screenshot
- PDF
- copied caption/text
```

Never make the entire architecture dependent on one scraping technique.

---

# 26. YouTube Processing

For YouTube content:

```text
URL
 ↓
Metadata
 ↓
Transcript if available
 ↓
Description
 ↓
Chapters
 ↓
Thumbnail
 ↓
AI analysis
```

For Shorts, use the same pipeline where the required data is available.

If only video is available:

```text
Video
 ↓
Audio extraction
 ↓
Speech-to-text
 ↓
Transcript
 ↓
LLM
```

---

# 27. Video Processing

When direct transcripts are unavailable:

```text
Video
 ↓
Extract audio
 ↓
Speech-to-text model
 ↓
Transcript
```

Optionally sample video frames.

For example:

```text
Video
 ↓
Frame sampling every N seconds
 ↓
Important-frame detection
 ↓
Vision model
```

This is especially useful when the video contains posters, slides, schedules, or screenshots.

Do not send every frame to a vision model because that is expensive and unnecessary.

---

# 28. Image Processing

Every extracted image should pass through:

```text
Image
 ↓
OCR
 ↓
Vision model
 ↓
Importance classification
```

Example result:

```json
{
  "is_important": true,
  "type": "event_poster",
  "reason": "Contains event dates and registration deadline",
  "ocr_text": "...",
  "description": "Event poster containing schedule and venue"
}
```

---

# 29. OCR

OCR should extract:

- dates
- times
- names
- URLs
- email addresses
- locations
- fees
- eligibility
- instructions

OCR text should be stored so it can be searched later.

---

# 30. Vision Analysis

Vision analysis should answer:

1. What is shown?
2. Is it informative?
3. Does it contain text?
4. Does it contain dates?
5. Does it contain a deadline?
6. Does it contain a schedule?
7. Does it contain a registration URL?
8. Does it contain requirements?
9. Is it merely decorative?

---

# 31. LLM Structured Extraction

Do not ask the LLM only for prose.

Ask for structured JSON.

Example:

```json
{
  "title": "AI Hackathon 2026",
  "category": "hackathon",
  "summary": "...",
  "important_points": [],
  "events": [],
  "deadlines": [],
  "action_items": [],
  "locations": [],
  "fees": [],
  "eligibility": [],
  "contacts": [],
  "links": [],
  "important_images": [],
  "confidence": 0.94
}
```

Use structured output / JSON schema if supported by the chosen AI API.

---

# 32. Date Extraction Is Critical

Dates may appear as:

```text
18 September
18/09/2026
Sep 18
Friday
Tomorrow
Registrations close soon
Last date: 18th Sept
```

The system must normalize them.

Example:

```text
18 September
```

becomes:

```text
2026-09-18
```

Only when the year can be safely inferred.

If ambiguous:

```text
"Friday"
```

the system should use the source date and context to resolve it, or ask the user for confirmation.

---

# 33. Confidence Levels

Every important extracted fact should have confidence.

Example:

```text
Registration deadline
18 Sep 2026
Confidence: 0.96
Source: Image #2
```

Another:

```text
Event date
25 Sep 2026
Confidence: 0.88
Source: Transcript
```

Low-confidence facts should require confirmation.

---

# 34. Calendar Integration

## Recommended first integration

**Google Calendar**

The user connects their Google account once.

The application receives appropriate calendar authorization.

Store tokens securely.

Do not store raw access tokens in plain text.

---

# 35. Calendar Workflow

```text
AI detects event/deadline
        ↓
Create suggestion
        ↓
User sees:
"Add to calendar?"
        ↓
User confirms
        ↓
Google Calendar API
        ↓
Event created
        ↓
Store external event ID
```

The system should never silently create dozens of calendar events.

---

# 36. Calendar Event Types

Use separate event categories.

### Actual event

```text
AI Hackathon
25 Sep 2026
10:00 AM
IIT Delhi
```

### Deadline

```text
Hackathon Registration Deadline
18 Sep 2026
11:59 PM
```

### Action

```text
Submit hackathon application
18 Sep 2026
```

---

# 37. Reminder Strategy

Default suggestions:

## Event

```text
7 days before
1 day before
2 hours before
```

## Deadline

```text
7 days before
2 days before
1 day before
6 hours before
```

The exact defaults should be configurable.

Most importantly:

> **Calendar/reminder creation requires user confirmation.**

---

# 38. Personal Timezone

Store the user's timezone.

For example:

```text
Asia/Kolkata
```

Every extracted datetime should be normalized with timezone information where possible.

Never silently treat an event from another timezone as local time.

---

# 39. Calendar Duplicate Prevention

Before creating an event:

```text
Check:
- same source
- same title
- same date
- same external calendar ID
```

If already created:

```text
Do not create duplicate.
```

---

# 40. Calendar Sync

Store:

```text
external_calendar_id
external_event_id
last_synced_at
```

Later, support:

```text
App
 ↕
Google Calendar
```

If an event is deleted from Google Calendar, the app should know whether it was:

- intentionally deleted
- still pending
- disconnected
- changed externally

---

# 41. Dashboard

The dashboard should have:

```text
┌─────────────────────────────────────────┐
│ Personal Content Vault                  │
├─────────────────────────────────────────┤
│ + Share URL                             │
│                                         │
│ Upcoming                                │
│ • Hackathon — Sep 25                    │
│ • Registration deadline — Sep 18        │
│                                         │
│ Recently Saved                          │
│ • AI workshop                           │
│ • Internship opportunity                │
│ • Cybersecurity event                   │
│                                         │
│ Categories                              │
│ AI | Cybersecurity | Internships        │
│ Events | Learning | Opportunities       │
└─────────────────────────────────────────┘
```

---

# 42. Content Detail Page

Every saved item should show:

```text
Title

Original source
[Open original]

Summary

Important information

Dates

Deadlines

Action items

Location

Eligibility

Fees

Useful links

Important images

Original transcript

Extracted text

AI notes

Tags
```

Also show where important information came from.

Example:

```text
Deadline: 18 September
Source: Image 2
```

This makes the AI more trustworthy.

---

# 43. Search

Start with normal PostgreSQL full-text search.

Search:

```text
hackathon
cybersecurity
IIT
internship
September deadline
```

Then add semantic search using pgvector.

---

# 44. Semantic Search

Semantic search lets me ask:

> "Find opportunities for college students related to AI."

without requiring exact keyword matches.

Pipeline:

```text
User query
 ↓
Embedding
 ↓
pgvector similarity search
 ↓
Relevant content
 ↓
Optional LLM synthesis
```

---

# 45. AI Chat Over Saved Content

Later add:

```text
Ask my knowledge
```

Examples:

> What deadlines do I have this month?

> Which hackathons did I save?

> What internships have I saved?

> Which events are happening in Delhi?

> Show me opportunities where registration is still open.

> What do I need to prepare for the hackathon I saved yesterday?

The AI should answer using retrieved saved content, not its general knowledge.

This is essentially a RAG system.

---

# 46. RAG Architecture

```text
Question
 ↓
Query embedding
 ↓
Vector search
 ↓
Keyword/date filtering
 ↓
Retrieve relevant notes
 ↓
LLM
 ↓
Answer with source references
```

The answer should cite the saved content.

Example:

```text
You have 3 AI hackathons saved.

1. AI Hackathon 2026
Deadline: 18 September

2. GenAI Challenge
Deadline: 22 September

3. ML Sprint
Deadline: 30 September
```

---

# 47. Important Source Traceability

Every extracted fact should ideally point back to:

```text
source URL
transcript section
image number
OCR text
```

This is important because AI can hallucinate.

The UI should allow:

```text
Deadline: 18 September
[View source]
```

and show the original image or transcript section.

---

# 48. AI Hallucination Protection

Use a strict rule:

> **The AI must not invent information that is not present in the source material.**

Prompt the model to:

- distinguish extracted facts from inference
- mark uncertain information
- return `null` when unavailable
- provide confidence
- identify the source of important facts

For example:

```json
{
  "deadline": {
    "value": "2026-09-18T23:59:00+05:30",
    "confidence": 0.97,
    "source": "image_2"
  }
}
```

---

# 49. Manual Correction

The user must be able to edit:

- title
- summary
- dates
- deadlines
- tags
- event details
- tasks
- importance
- notes

AI should assist, not control the data permanently.

---

# 50. Processing Status

When processing a shared link, show progress.

```text
✓ URL received
✓ Identified as Instagram Reel
✓ Extracted caption
✓ Extracted video
✓ Generated transcript
✓ Found 4 useful frames
✓ Analyzed images
✓ Detected 2 dates
✓ Generated summary

Ready for review
```

---

# 51. Background Jobs

Content processing may take time.

Do not make the main API request wait for everything.

Use a queue.

```text
API
 ↓
Create processing job
 ↓
Return job ID
 ↓
Worker processes content
 ↓
Frontend polls / receives status
```

Recommended options:

- Celery + Redis
- RQ + Redis
- Dramatiq
- a managed queue later

For an MVP, Redis + Celery is enough.

---

# 52. Processing Jobs

Possible job types:

```text
extract_content
extract_media
transcribe_video
process_image
run_ocr
run_vision
analyze_content
generate_note
generate_embedding
calendar_sync
```

---

# 53. Retry System

Failures should be retryable.

Example:

```text
Extraction failed
 ↓
Retry 1
 ↓
Retry 2
 ↓
Retry 3
 ↓
Mark partial/failed
```

Do not endlessly retry.

---

# 54. Partial Processing

If Instagram extraction gets the caption but not the video:

Don't fail the whole record.

Save:

```text
Status: Partial

Available:
✓ Caption
✓ Author
✓ URL

Unavailable:
✗ Video
✗ Transcript
```

Then allow manual upload.

---

# 55. Deduplication

If the same URL is shared twice:

```text
Same normalized URL
        ↓
Find existing source
        ↓
Do not create duplicate
```

For reposted content with different URLs, use:

- content hash
- title similarity
- embedding similarity

to detect probable duplicates.

---

# 56. Security

Even though this is a single-user app, treat it as production software.

Important protections:

- HTTPS
- authentication
- secure sessions
- encrypted OAuth tokens
- environment variables
- no secrets in Git
- input validation
- URL validation
- SSRF protection
- file type validation
- upload size limits
- malware scanning for uploads
- rate limiting
- database backups
- least-privilege API scopes

---

# 57. SSRF Protection

This is especially important because the server fetches URLs supplied by the user.

Never allow arbitrary internal network requests.

Block:

```text
localhost
127.0.0.1
private IP ranges
metadata endpoints
internal hostnames
```

Validate redirects as well.

---

# 58. File Security

For uploaded:

- images
- videos
- PDFs

validate:

```text
MIME type
file extension
file size
actual file signature
```

Never trust the extension alone.

---

# 59. Privacy

Because the system is personal:

- minimize collected data
- encrypt sensitive tokens
- allow deletion
- keep source URLs private
- do not expose API endpoints publicly
- use private object storage
- back up database securely

The AI provider's data-retention policy should be checked before choosing a provider.

---

# 60. API Design

Example endpoints:

```text
POST   /api/sources
GET    /api/sources
GET    /api/sources/{id}
DELETE /api/sources/{id}

POST   /api/sources/{id}/process
GET    /api/jobs/{id}

GET    /api/search?q=...
GET    /api/tags

GET    /api/events
POST   /api/events/{id}/calendar
DELETE /api/events/{id}

GET    /api/deadlines
POST   /api/deadlines/{id}/calendar

GET    /api/action-items
PATCH  /api/action-items/{id}

POST   /api/calendar/connect
POST   /api/calendar/disconnect

POST   /api/chat
```

---

# 61. Frontend Pages

Recommended:

```text
/
  Dashboard

/inbox
  Processing queue

/library
  All saved content

/library/:id
  Content detail

/calendar
  Events + deadlines

/tasks
  Action items

/search
  Search

/chat
  Ask my knowledge

/settings
  Calendar / AI / storage / preferences
```

---

# 62. Share Mechanism

## MVP

Use:

```text
Paste URL
```

## Next

Browser bookmarklet / extension.

## Later

Mobile share sheet.

Ideal experience:

```text
Instagram
 ↓
Share
 ↓
Personal Content Vault
 ↓
Saved
```

No copy-paste required.

---

# 63. Mobile Strategy

Do not build a full native mobile app first.

First make the web app responsive.

Then build:

```text
iOS Share Extension
Android Share Target
```

Both simply send the URL to the backend.

---

# 64. Notifications

Start with calendar notifications because Google Calendar already provides reliable reminders.

Later add:

- email
- push notifications
- browser notifications
- Telegram
- WhatsApp where supported

Avoid building a custom notification engine too early.

---

# 65. Suggested AI Components

The exact models can change over time.

Use model abstraction:

```text
AIProvider
 ├── LLM
 ├── Vision
 ├── Embeddings
 └── SpeechToText
```

This prevents the entire project from being tied to one vendor.

Example interfaces:

```python
class LLMProvider:
    def analyze(self, content): ...

class VisionProvider:
    def analyze(self, image): ...

class EmbeddingProvider:
    def embed(self, text): ...

class SpeechProvider:
    def transcribe(self, audio): ...
```

---

# 66. Prompt Design

Keep prompts in version-controlled files.

```text
prompts/
├── content_analysis.txt
├── date_extraction.txt
├── image_analysis.txt
├── event_extraction.txt
├── action_extraction.txt
└── summarization.txt
```

Do not hardcode huge prompts inside Python files.

---

# 67. Master Analysis Prompt Requirements

The main content-analysis prompt should tell the AI:

```text
You are analyzing content saved by a single user.

Use only information provided in the source material.

Extract:
- title
- summary
- category
- important facts
- dates
- deadlines
- events
- tasks
- eligibility
- location
- price
- contact information
- links
- important images

For every date/deadline:
- normalize the date
- include timezone when known
- identify the source
- provide confidence

Do not invent missing information.

If information is unavailable, return null.

Distinguish facts from assumptions.
```

---

# 68. Structured Output Example

```json
{
  "title": "AI Hackathon 2026",
  "category": "hackathon",
  "summary": "A three-day AI hackathon for college students.",
  "facts": [
    {
      "type": "fee",
      "value": "299 INR",
      "confidence": 0.98,
      "source": "image_1"
    }
  ],
  "events": [
    {
      "title": "AI Hackathon 2026",
      "start": "2026-09-25T10:00:00+05:30",
      "end": "2026-09-27T18:00:00+05:30",
      "confidence": 0.91
    }
  ],
  "deadlines": [
    {
      "title": "Registration deadline",
      "datetime": "2026-09-18T23:59:00+05:30",
      "confidence": 0.97
    }
  ],
  "action_items": [
    {
      "title": "Register for the hackathon"
    }
  ]
}
```

---

# 69. Calendar Confirmation UI

After analysis:

```text
┌────────────────────────────────────────┐
│ Calendar suggestions                   │
├────────────────────────────────────────┤
│                                        │
│ ☑ AI Hackathon 2026                    │
│   25 Sep • 10:00 AM                    │
│                                        │
│ ☑ Registration Deadline                │
│   18 Sep • 11:59 PM                    │
│                                        │
│ Reminder:                              │
│ 7 days + 1 day before                  │
│                                        │
│        [Add to Calendar]               │
└────────────────────────────────────────┘
```

---

# 70. Personal Knowledge Organization

Automatic categories:

```text
Events
Hackathons
Internships
Jobs
Competitions
Scholarships
Courses
Learning
Tech
Cybersecurity
AI
Projects
Ideas
Other
```

Allow custom tags.

---

# 71. Importance Levels

Each saved item:

```text
⭐ Important
📌 Normal
🗃️ Archive
```

AI can suggest importance but the user decides.

---

# 72. Expiration Handling

Some content becomes useless after a deadline.

For example:

```text
Registration deadline: 18 Sep
```

After that date:

```text
Status:
Expired
```

But do not delete the content automatically.

Keep it for historical search.

---

# 73. Event Lifecycle

```text
Discovered
   ↓
Upcoming
   ↓
Completed
   ↓
Archived
```

For deadlines:

```text
Upcoming
   ↓
Due
   ↓
Expired
```

---

# 74. Calendar vs Reminder Logic

Not everything needs a calendar event.

### Calendar

Use for:

- event attendance
- meetings
- workshops
- conferences
- deadlines that matter

### Task

Use for:

- apply
- register
- download
- submit
- prepare

### Note

Use for:

- useful information
- ideas
- educational content
- references

AI should classify the information accordingly.

---

# 75. Example Decision Logic

```text
Does content contain a scheduled event?
    YES → Event suggestion

Does it contain a deadline?
    YES → Deadline suggestion

Does it contain an action?
    YES → Task suggestion

Does it contain useful information?
    YES → Knowledge note

Can it be useful visually?
    YES → Preserve image
```

One source can produce all four.

---

# 76. Important Images Storage

For every important image store:

```text
image
source URL
content ID
OCR
AI description
reason marked important
timestamp
```

Show them in the note.

Example:

```text
Important Visuals

[Event Poster]

Why important:
Contains registration deadline and venue.
```

---

# 77. Cost Control

AI processing can become expensive.

Use staged processing.

### Cheap operations first

```text
URL classification
metadata
basic extraction
```

Then:

```text
OCR
```

Then only use expensive vision/LLM analysis where necessary.

For video:

```text
Transcript first
```

Only analyze frames when transcript/content indicates visual information may matter.

---

# 78. Caching

Never process the same content repeatedly.

Cache:

```text
URL → extracted content
content hash → analysis
image hash → OCR
transcript → analysis
```

This reduces cost and processing time.

---

# 79. Observability

Keep logs for:

```text
processing time
extractor used
AI model used
token usage
failure reason
retry count
```

Do not log:

- OAuth secrets
- private tokens
- unnecessary personal content

---

# 80. Testing Strategy

## Unit tests

Test:

- URL detection
- date parsing
- deadline extraction
- duplicate detection
- calendar event construction
- permissions
- validation

## Integration tests

Test:

```text
URL
 ↓
Extractor
 ↓
AI
 ↓
Database
 ↓
Calendar
```

## AI evaluation

Create a fixed test dataset.

Example:

```text
20 Instagram posts
20 YouTube videos
20 event posters
20 screenshots
```

Manually define expected:

```text
deadline
event date
location
fee
category
action
```

Run the AI pipeline and measure extraction accuracy.

---

# 81. AI Evaluation Metrics

Track:

### Date accuracy

```text
Correct dates / total dates
```

### Deadline precision

```text
Correct deadlines / detected deadlines
```

### Deadline recall

```text
Detected deadlines / actual deadlines
```

### Classification accuracy

```text
Correct category / total items
```

### Image importance accuracy

```text
Correct important images / total images
```

---

# 82. MVP Scope

Do NOT build everything at once.

## MVP v1

Build only:

```text
1. Login
2. Paste URL
3. Web/YouTube extraction
4. AI summary
5. Structured extraction
6. PostgreSQL storage
7. Dashboard
8. Search
```

---

# 83. MVP v2

Add:

```text
1. Instagram support where technically available
2. OCR
3. Image extraction
4. Vision analysis
5. Important image preservation
6. Deadline detection
7. Event detection
8. Action items
```

---

# 84. MVP v3

Add:

```text
1. Google Calendar OAuth
2. Calendar event suggestions
3. Deadline reminders
4. Confirmation UI
5. Duplicate prevention
6. Calendar sync
```

---

# 85. MVP v4

Add:

```text
1. Semantic search
2. RAG
3. AI chat
4. Browser extension
5. Mobile share
6. Weekly digest
```

---

# 86. Development Order

Follow this exact order.

## Step 1

Create repository.

```text
personal-content-vault/
├── frontend/
├── backend/
├── worker/
├── prompts/
├── infrastructure/
└── README.md
```

## Step 2

Set up:

```text
Next.js
FastAPI
PostgreSQL
Redis
```

## Step 3

Create database models.

## Step 4

Create URL submission API.

## Step 5

Create processing queue.

## Step 6

Implement website extraction.

## Step 7

Implement YouTube extraction.

## Step 8

Implement transcript processing.

## Step 9

Connect LLM.

## Step 10

Generate structured JSON.

## Step 11

Save notes.

## Step 12

Build dashboard.

## Step 13

Build search.

## Step 14

Add OCR.

## Step 15

Add image/vision analysis.

## Step 16

Add deadline/event extraction.

## Step 17

Add Google Calendar OAuth.

## Step 18

Add calendar confirmation.

## Step 19

Add reminders.

## Step 20

Add semantic search.

## Step 21

Add AI chat.

## Step 22

Add browser/mobile sharing.

---

# 87. Suggested Repository

```text
personal-content-vault/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── hooks/
│   └── types/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── extractors/
│   │   ├── ai/
│   │   ├── calendar/
│   │   ├── search/
│   │   └── storage/
│   └── tests/
│
├── worker/
│   ├── tasks/
│   └── pipelines/
│
├── prompts/
│   ├── analyze_content.txt
│   ├── analyze_image.txt
│   ├── extract_dates.txt
│   └── generate_summary.txt
│
├── infrastructure/
│   ├── docker/
│   └── compose/
│
├── .env.example
├── docker-compose.yml
└── README.md
```

---

# 88. Environment Variables

Example:

```text
DATABASE_URL=
REDIS_URL=

AI_API_KEY=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=

STORAGE_BUCKET=
STORAGE_ACCESS_KEY=
STORAGE_SECRET_KEY=

APP_SECRET=
```

Never commit `.env`.

Commit only:

```text
.env.example
```

---

# 89. Local Development

Recommended local setup:

```text
Docker Compose
```

Run:

```text
Frontend
Backend
PostgreSQL
Redis
```

Later add:

```text
Worker
```

This gives a reproducible environment.

---

# 90. Production Architecture

For personal use, keep it simple.

```text
Internet
   ↓
Reverse Proxy / HTTPS
   ↓
Frontend
   ↓
Backend API
   ↓
PostgreSQL
   ↓
Redis
   ↓
Worker
   ↓
Object Storage
```

The database and storage should not be publicly accessible.

---

# 91. Backup Strategy

At minimum:

```text
Daily PostgreSQL backup
Weekly full backup
```

Keep multiple historical versions.

Important media should also be backed up.

---

# 92. Failure Scenarios

### URL unavailable

Show:

```text
Unable to retrieve content automatically.
Upload the video/image/PDF instead.
```

### Transcript unavailable

Try speech-to-text.

### Image extraction unavailable

Ask user for screenshots.

### AI failure

Retry.

### Calendar failure

Save the calendar suggestion locally and allow retry.

### Duplicate

Show:

```text
This content already exists.
```

---

# 93. User Experience Principle

The application should minimize effort.

Ideal:

```text
Share
 ↓
Forget about it
 ↓
System processes
 ↓
Notification:
"Saved. I found a deadline."
 ↓
One tap:
"Add to calendar"
```

The user should not have to manually enter:

- title
- date
- deadline
- location
- tags
- summary

unless AI cannot determine them reliably.

---

# 94. What NOT to Build Initially

Avoid:

- multi-user organizations
- complex permissions
- team collaboration
- custom mobile app
- custom notification infrastructure
- multiple calendar providers
- multiple vector databases
- complex analytics
- elaborate AI agents
- automatic calendar creation without confirmation

These add complexity without helping the core product.

---

# 95. Best Initial Architecture

For the first working version:

```text
Frontend:
Next.js + TypeScript

Backend:
FastAPI + Python

Database:
PostgreSQL + pgvector

Queue:
Redis + Celery

AI:
LLM + Vision + Speech-to-text + Embeddings

OCR:
OCR engine/API

Calendar:
Google Calendar API

Storage:
Local filesystem initially
→ S3-compatible storage later

Deployment:
Docker
```

---

# 96. The Complete Data Flow

```text
USER
 │
 │ Share URL
 ▼
FRONTEND
 │
 │ POST /sources
 ▼
BACKEND
 │
 ├── Validate URL
 │
 ├── Detect platform
 │
 └── Create processing job
          │
          ▼
        REDIS
          │
          ▼
        WORKER
          │
          ├── Extract content
          │
          ├── Extract images
          │
          ├── Extract transcript
          │
          ├── OCR
          │
          ├── Vision
          │
          └── Normalize
                  │
                  ▼
              LLM ANALYSIS
                  │
                  ├── Summary
                  ├── Facts
                  ├── Events
                  ├── Deadlines
                  ├── Tasks
                  ├── Tags
                  └── Important images
                         │
                         ▼
                    POSTGRESQL
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
         Library      Calendar      Search
                         │
                         ▼
                    Google Calendar
```

---

# 97. Final Product Vision

Eventually the system should feel like a private personal assistant for internet information.

I should be able to:

```text
See something useful
       ↓
Share it
       ↓
Never manually organize it
       ↓
AI understands it
       ↓
Important information is preserved
       ↓
Deadlines appear on my calendar
       ↓
Tasks become reminders
       ↓
Everything remains searchable
```

And later:

```text
"What did I save about internships?"

"What deadlines do I have this week?"

"Which hackathons are still open?"

"What was that cybersecurity event I saw on Instagram?"

"Show me all opportunities with deadlines before October."

"What do I need to do tomorrow?"
```

The system should answer from my own saved content.

---

# 98. Definition of Done

The project can be considered a successful first release when:

- [ ] I can paste/share a URL.
- [ ] The system identifies the source.
- [ ] Content is extracted.
- [ ] AI creates a structured note.
- [ ] The original source is preserved.
- [ ] Images can be extracted.
- [ ] Useful images are identified.
- [ ] OCR works.
- [ ] Dates are extracted.
- [ ] Deadlines are extracted.
- [ ] Events are extracted.
- [ ] Tasks are extracted.
- [ ] Everything is saved in PostgreSQL.
- [ ] I can search saved content.
- [ ] I can edit AI-generated information.
- [ ] Google Calendar can be connected.
- [ ] Calendar suggestions require confirmation.
- [ ] Calendar events are created successfully.
- [ ] Deadline reminders are created.
- [ ] Duplicate calendar events are prevented.
- [ ] Failed processing can be retried.
- [ ] Private data is protected.
- [ ] Database and media are backed up.

---

# 99. Most Important Development Rule

Build the system incrementally.

Do not start by trying to support:

```text
Instagram + YouTube + LinkedIn + X + PDFs
+ OCR + video + vision + calendar + RAG
```

all at once.

Start:

```text
URL
 ↓
Web extraction
 ↓
LLM
 ↓
Structured note
 ↓
Database
```

Then progressively add:

```text
YouTube
 ↓
Images
 ↓
OCR
 ↓
Vision
 ↓
Dates
 ↓
Deadlines
 ↓
Calendar
 ↓
Reminders
 ↓
Semantic search
 ↓
AI chat
 ↓
Mobile sharing
```

This makes debugging dramatically easier.

---

# 100. Final Architecture Decision

The recommended long-term architecture is:

```text
                    PERSONAL AI CONTENT VAULT

       ┌─────────────────────────────────────────┐
       │              INPUT LAYER                │
       │                                         │
       │ URL | Share Sheet | Browser | Upload    │
       └───────────────────┬─────────────────────┘
                           │
                           ▼
       ┌─────────────────────────────────────────┐
       │           CONTENT INGESTION             │
       │                                         │
       │ Instagram | YouTube | Web | PDF        │
       └───────────────────┬─────────────────────┘
                           │
                           ▼
       ┌─────────────────────────────────────────┐
       │          MULTIMODAL PROCESSING          │
       │                                         │
       │ Text | Transcript | OCR | Images | AI  │
       └───────────────────┬─────────────────────┘
                           │
                           ▼
       ┌─────────────────────────────────────────┐
       │          KNOWLEDGE EXTRACTION           │
       │                                         │
       │ Summary | Facts | Dates | Events        │
       │ Deadlines | Tasks | Tags | Links        │
       └───────────────────┬─────────────────────┘
                           │
                           ▼
       ┌─────────────────────────────────────────┐
       │              KNOWLEDGE BASE             │
       │                                         │
       │ PostgreSQL + pgvector + Object Storage  │
       └───────────────────┬─────────────────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Library       Calendar       AI Search
                            │             │
                            ▼             ▼
                       Reminders       AI Chat
```

## Core philosophy

**Capture once. Understand automatically. Store permanently. Act when necessary. Find it later.**

That is the central product around which the entire implementation should be designed.
