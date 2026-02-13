from fastapi import FastAPI
from fastapi import UploadFile, File
from app.services.storage import upload_file_to_s3
from app.telegram.schemas import Update
from app.telegram.client import send_message


from app.agents.router import RouterAgent
from app.agents.intents import Intent
from app.agents.support import SupportAgent
from app.agents.finance import FinanceAgent
from app.agents.docs import DocsAgent

from app.infra.db import SessionLocal

app = FastAPI(title="CondoAI Assitant", version="0.1.0")

router = RouterAgent()
support_agent = SupportAgent()
finance_agent = FinanceAgent()
docs_agent = DocsAgent()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    data = await file.read()

    result = upload_file_to_s3(
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        data=data
    )
    return {"ok": True, "file": {"filename": file.filename, **result}}

@app.post("/webhook/telegram")
async def telegram_webhook(update: Update):
    if not update.message or not update.message.text:
        return {"ok": True}
    
    chat_id = update.message.chat.id
    text = update.message.text.strip()

    intent = await router.route(text)

    db = SessionLocal()
    try:
        if intent == Intent.SUPPORT:
            reply = support_agent.handle(text)
        elif intent == Intent.FINANCE:
            reply = finance_agent.handle(text, db=db)
        elif intent == Intent.DOCS:
            reply = docs_agent.handle(text)
        else:
            reply = (
                "🤔 Ainda tô aprendendo esse tipo de pedido.\n\n"
                "Sugestões:\n"
                "- 'meu boleto vence quando?'\n"
                "- 'tenho um pdf da ata'\n"
                "- 'faz um comunicado pros moradores'\n"
            )
    finally:
        db.close()

    await send_message(chat_id, reply)
    return {"ok": True}

