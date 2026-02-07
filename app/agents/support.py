from app.services.tools import generate_resident_notice

class SupportAgent:
    def handle(self, text: str) -> str:
        t = text.lower()

        # regra simples: se usuario pedir um "comunicado", geramos um template
        if "comunicado" in t:
            return generate_resident_notice(
                topic="Aviso geral",
                details="Por favor, mantenham silêncio após as 22h e respeitem as áreas comuns."
            )
        
        return (
            "👋 Oi! Eu sou o CondoAI.\n"
            "Você pode perguntar sobre boletos/vencimentos, documentos, ou pedir um *comunicado*."
        ) 