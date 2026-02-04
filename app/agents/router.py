from app.agents.intents import Intent

class RouterAgent:
    """
    RouterAgent v1: roteamento por heurísticas (regras simples);
    Uso heurística primeiro pra reduzir custo e latência, LLM só quando precisa.
    """

    def route(self, text: str) -> Intent:
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