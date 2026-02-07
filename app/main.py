from fastapi import FastAPI
from app.telegram.schemas import Update
from app.telegram.client import send_message


from app.agents.router import RouterAgent
from app.agents.intents import Intent
from app.agents.support import SupportAgent
from app.agents.finance import FinanceAgent
from app.agents.docs import DocsAgent

app = FastAPI(title="CondoAI Assitant", version="0.1.0")

router = RouterAgent()
support_agent = SupportAgent()
finance_agent = FinanceAgent()
docs_agent = DocsAgent()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/webhook/telegram")
async def telegram_webhook(update: Update):
    if not update.message or not update.message.text:
        return {"ok": True}
    
    chat_id = update.message.chat.id
    text = update.message.text.strip()

    intent = await router.route(text)

    if intent == Intent.SUPPORT:
        reply = support_agent.handle(text)
    elif intent == Intent.FINANCE:
        reply = finance_agent.handle(text)
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

    await send_message(chat_id, reply
                       )

    return {"ok": True}

