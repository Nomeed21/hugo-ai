import os
import time
from contextlib import asynccontextmanager
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

from rag_pipeline import get_rag_response
from session_memory import SessionMemory


# Initialize session memory with 10-turn limit and 30-minute timeout
session_memory = SessionMemory(max_turns=10, timeout_minutes=30)


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


# Create the FastAPI application
app = FastAPI(title="Hugo AI", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Request model: what the frontend sends
class ChatRequest(BaseModel):
    message: str
    session_id: str


# Individual source reference in the response
class SourceItem(BaseModel):
    page_source: str
    section_title: str


# Response model: what the API returns
class ChatResponse(BaseModel):
    response: str
    sources: list[SourceItem]
    confidence: float

class FeedbackRequest(BaseModel):
    session_id: str
    message: str
    response: str
    rating: str  # "thumbs_up" or "thumbs_down"


class FeedbackStats(BaseModel):
    total: int
    thumbs_up: int
    thumbs_down: int
    positive_ratio: float
    
@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0", "service": "hugo-ai"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Retrieve conversation history for this session
    history = session_memory.get_history(request.session_id)

    # Run the full RAG pipeline
    result = get_rag_response(
        query=request.message,
        session_history=history,
    )

    # Store this turn in session memory
    session_memory.add_turn(
        session_id=request.session_id,
        user_message=request.message,
        assistant_message=result["response"],
    )

    # Build source objects from the result
    sources = [
        SourceItem(page_source=s["page_source"], section_title=s["section_title"])
        for s in result["sources"]
    ]

    return ChatResponse(
        response=result["response"],
        sources=sources,
        confidence=result["confidence"],
    )

@app.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    from supabase import create_client

    supabase_client = create_client(
        os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    )

    supabase_client.table("feedback").insert(
        {
            "session_id": request.session_id,
            "message": request.message,
            "response": request.response,
            "rating": request.rating,
            "created_at": datetime.utcnow().isoformat(),
        }
    ).execute()

    return {"status": "feedback recorded"}

@app.get("/feedback/stats", response_model=FeedbackStats)
def feedback_stats():
    from supabase import create_client

    supabase_client = create_client(
        os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    )

    result = supabase_client.table("feedback").select("rating").execute()
    records = result.data if result.data else []

    total = len(records)
    thumbs_up = sum(1 for r in records if r["rating"] == "thumbs_up")
    thumbs_down = total - thumbs_up
    positive_ratio = thumbs_up / total if total > 0 else 0.0

    return FeedbackStats(
        total=total,
        thumbs_up=thumbs_up,
        thumbs_down=thumbs_down,
        positive_ratio=round(positive_ratio, 2),
    )
