from typing import List, Dict

def aggregate_scores(scored_comments: List[Dict], threshold: float = 0.7) -> Dict:
    toxic = [c for c in scored_comments if c["toxic_probability"] >= threshold]
    total = len(scored_comments) or 1

    return {
        "total_comments": len(scored_comments),
        "toxic_comments": len(toxic),
        "toxicity_ratio": len(toxic) / total,
        "avg_toxicity": sum(c["toxic_probability"] for c in scored_comments) / total,
        "top_toxic": sorted(toxic, key=lambda x: x["toxic_probability"], reverse=True)[:5],
    }
