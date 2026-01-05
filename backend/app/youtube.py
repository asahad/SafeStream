import re
import requests
from typing import List
from .settings import settings

def extract_video_id(url: str) -> str:
    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?&/]+)",
        r"youtube\.com/shorts/([^?&/]+)",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    raise ValueError("Invalid YouTube URL")

def fetch_top_level_comments(video_id: str, max_comments: int) -> List[str]:
    comments = []
    endpoint = "https://www.googleapis.com/youtube/v3/commentThreads"

    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": settings.YOUTUBE_API_KEY,
        "maxResults": 100,
        "textFormat": "plainText",
        "order": "time",
    }

    page_token = None
    while len(comments) < max_comments:
        if page_token:
            params["pageToken"] = page_token

        r = requests.get(endpoint, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()

        for item in data.get("items", []):
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            if text:
                comments.append(text)
            if len(comments) >= max_comments:
                break

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return comments
