from datetime import date, timedelta
from typing import List, Dict

def get_upcoming_bills(days: int = 7) -> List[Dict]:
    """
    Tool v1 (mock): simula boletos a vencer.
    Depois vira consulta real no Postgres.
    """

    today = date.today()
    return [
        {"id": "BLT-1001", "due_date": str(today + timedelta(days=2)), "amount": 420.50, "status": "open"},
        {"id": "BLT-1002", "due_date": str(today + timedelta(days=5)), "amount": 199.90, "status": "open"},
    ]

def format_bills_message(bills: List[Dict]) -> str:
    if not bills:
        return "Nada a vencer nos próximos dias."
    lines = ["Boletos a vencer:"]
    for b in bills:
        lines.append(f" - {b['id']} | vence {b['due_date']} | R$ {b['amount']:.2f} | {b['status']}")
    return "\n".join(lines)

def generate_resident_notice(topic: str, details: str) -> str:
    """
    Tool: gera um comunicado padrão (sem IA)
    IA entra depois só pra reescrever com um tom/clareza.
    """

    return (
        "📢 COMUNICADO AOS MORADORES\n\n"
        f"Assunto: {topic}\n\n"
        f"{details}\n\n"
        "Agradecemos a colaboração.\n"
        "- Administração do Condomínio"
    )