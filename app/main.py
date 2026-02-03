from fastapi import FastAPI

from app.telegram.schemas import Update
from app.telegram.client import send_message

app = FastAPI(title="CondoAI Assitant", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/webhook/telegram")
async def telegram_webhook(update: Update):
    if not update.message or not update.message.text:
        return {"ok": True}
    
    chat_id = update.message.chat.id
    text = update.message.text.strip()

    await send_message(chat_id, f"Recebi: {text}")

    return {"ok": True}

