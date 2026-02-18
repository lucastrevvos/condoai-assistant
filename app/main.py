import uuid
from sqlalchemy.orm import Session
from fastapi import FastAPI, UploadFile, File
from app.services.storage import upload_file_to_s3
from app.telegram.schemas import Update
from app.telegram.client import send_message

from app.services.queue import enqueue_document_job

from app.agents.router import RouterAgent
from app.agents.intents import Intent
from app.agents.support import SupportAgent
from app.agents.finance import FinanceAgent
from app.agents.docs import DocsAgent

from app.infra.db import SessionLocal

from app.domain.models import Document

app = FastAPI(title="CondoAI Assitant", version="0.1.0")

router = RouterAgent()
support_agent = SupportAgent()
finance_agent = FinanceAgent()
docs_agent = DocsAgent()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(chat_id: str, file: UploadFile = File(...)):
    data = await file.read()

    # 1) S3
    result = upload_file_to_s3(
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        data=data
    )

    # 2) DB: cria registro
    document_id = str(uuid.uuid4())
    db: Session = SessionLocal()

    try:
        doc = Document(
            id=document_id,
            chat_id=str(chat_id),
            bucket=result["bucket"],
            key=result["key"],
            filename=file.filename,
            status="queued"
        )
        db.add(doc)
        db.commit()
    finally:
        db.close()

    # 3) SQS: enfileira
    job = enqueue_document_job({
        "type": "document_uploaded",
        "document_id": document_id
    })

    return {"ok": True, "document_id": document_id, "job": job}

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

