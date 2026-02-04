from typing import Optional
from openai import AsyncOpenAI
from app.core.config import OPENAI_API_KEY, OPEN_MODEL

_client: Optional[AsyncOpenAI] = None

def get_llm_client() -> Optional[AsyncOpenAI]:
    global _client
    if not OPENAI_API_KEY:
        return None
    if _client is None:
        _client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    return _client

async def classify_intent(text: str) -> str:
    """
    Returns one of: support, finance, docs, unknown
    """

    client = get_llm_client()
    if client is None:
        return "unknown"
    
    system = (
        "You are an intent classifier for a condo assistant."
        "Return ONLY one label: support, finance, docs, unknown."
    )

    user = f"Message: {text}"

    resp = await client.chat.completions.create(
        model=OPEN_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0,
        max_tokens=5
    )

    label = resp.choices[0].message.content.strip().lower()

    if label not in {"support", "finance", "docs", "unknown"}:
        return "unknown"
    return label