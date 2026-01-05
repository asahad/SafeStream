import hashlib
import random
from typing import List, Dict

def score_comments(comments: List[str]) -> List[Dict]:
    scored = []
    for text in comments:
        h = int(hashlib.md5(text.encode()).hexdigest(), 16)
        random.seed(h)
        prob = random.random()
        scored.append({
            "text": text,
            "toxic_probability": prob
        })
    return scored
