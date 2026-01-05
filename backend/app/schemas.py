from pydantic import BaseModel, HttpUrl, Field
from typing import List

class AnalyzeVideoRequest(BaseModel):
    url: HttpUrl
    max_comments: int = Field(default=100, ge=10, le=300)

class LivePollRequest(BaseModel):
    url: HttpUrl
    max_comments: int = Field(default=100, ge=10, le=300)

class ScoredComment(BaseModel):
    text: str
    toxic_probability: float

class VideoMetrics(BaseModel):
    total_comments: int
    toxic_comments: int
    toxicity_ratio: float
    avg_toxicity: float
    top_toxic: List[ScoredComment]

class AnalyzeVideoResponse(BaseModel):
    metrics: VideoMetrics
    llm_summary: str
    sampled_comments: int

class LivePollResponse(BaseModel):
    metrics: VideoMetrics
    llm_summary: str
    sampled_comments: int
    polled_at: str
    new_comments_estimate: int
