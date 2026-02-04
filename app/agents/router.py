from app.agents.intents import Intent
from app.services.llm import classify_intent

class RouterAgent:
    """
    RouterAgent v2: heurísticas primeiro, LLM fallback quando UNKNOWN.
    """

    def route_by_rules(self, text: str) -> Intent:
        t = text.lower().strip()

        finance_keywords = ["boleto", "pagamento", "vencimento", "saldo", "taxa", "condomínio", "condominio"]
        docs_keywords = ["ata", "pdf", "documento", "anexo", "arquivo", "comunicado"]
        support_keywords = ["ajuda", "como", "oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]

        if any(k in t for k in finance_keywords):
            return Intent.FINANCE
        if any(k in t for k in docs_keywords):
            return Intent.DOCS
        if any(k in t for k in support_keywords):
            return Intent.SUPPORT
        
        return Intent.UNKNOWN
    
    async def route(self, text: str) -> Intent:
        intent = self.route_by_rules(text)

        if intent != Intent.UNKNOWN:
            return intent
        
        label = await classify_intent(text)

        mapping = {
            "support": Intent.SUPPORT,
            "finance": Intent.FINANCE,
            "docs": Intent.DOCS,
            "unknown": Intent.UNKNOWN
        }

        return mapping.get(label, Intent.UNKNOWN)
