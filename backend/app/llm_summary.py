from openai import OpenAI
from .settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_llm_summary(metrics: dict) -> str:
    examples = metrics["top_toxic"]
    lines = "\n".join(
        f"- ({c['toxic_probability']:.2f}) {c['text']}" for c in examples
    ) or "- none"

    prompt = f"""
You are a Trust & Safety analyst.

Based on these YouTube comment toxicity metrics, provide:
1. Risk level (Low / Medium / High)
2. Why (1–3 bullets)
3. Recommended action
4. Short moderator note

Metrics:
Total comments: {metrics['total_comments']}
Toxic comments: {metrics['toxic_comments']}
Toxicity ratio: {metrics['toxicity_ratio']:.2f}
Average toxicity: {metrics['avg_toxicity']:.2f}

Most toxic examples:
{lines}
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content.strip()
