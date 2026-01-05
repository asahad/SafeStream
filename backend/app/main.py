from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import hashlib

from .settings import settings
from .schemas import (
    AnalyzeVideoRequest, AnalyzeVideoResponse,
    LivePollRequest, LivePollResponse
)
from .youtube import extract_video_id, fetch_top_level_comments
from .scoring import score_comments
from .aggregate import aggregate_scores
from .llm_summary import generate_llm_summary
from .cache import cache, seen
from .rate_limit import enforce_min_interval

app = FastAPI(
    title="SafeStream API",
    version="1.0.0",
    description="Backend service for SafeStream"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN] if settings.FRONTEND_ORIGIN != "*" else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

def _fp(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()

@app.post("/analyze-video", response_model=AnalyzeVideoResponse)
def analyze_video(req: AnalyzeVideoRequest, request: Request):
    try:
        enforce_min_interval(request.client.host)
        video_id = extract_video_id(str(req.url))
        key = f"analyze:{video_id}:{req.max_comments}"

        if key in cache:
            return cache[key]

        comments = fetch_top_level_comments(video_id, req.max_comments)
        scored = score_comments(comments)
        metrics = aggregate_scores(scored)
        summary = generate_llm_summary(metrics)

        payload = {
            "metrics": metrics,
            "llm_summary": summary,
            "sampled_comments": len(comments),
        }
        cache[key] = payload
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/live-poll", response_model=LivePollResponse)
def live_poll(req: LivePollRequest, request: Request):
    try:
        enforce_min_interval(request.client.host)
        video_id = extract_video_id(str(req.url))
        key = f"live:{video_id}:{req.max_comments}"

        comments = fetch_top_level_comments(video_id, req.max_comments)
        scored = score_comments(comments)
        metrics = aggregate_scores(scored)
        summary = generate_llm_summary(metrics)

        fps = {_fp(c) for c in comments}
        prev = seen.get(key, set())
        new_estimate = len(fps - prev)
        seen[key] = fps

        return {
            "metrics": metrics,
            "llm_summary": summary,
            "sampled_comments": len(comments),
            "polled_at": datetime.now(timezone.utc).isoformat(),
            "new_comments_estimate": new_estimate,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
