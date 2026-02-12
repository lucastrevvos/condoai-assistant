from datetime import date, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session

from app.domain.models import Bill

def get_upcoming_bills(db: Session, days: int = 7) -> List[Dict]:
    """
    Tool v2: consulta eral no Postgres
    """

    today = date.today()
    limit_date = today + timedelta(days=days)

    rows = (
        db.query(Bill)
        .filter(Bill.due_date >= today, Bill.due_date <= limit_date)
        .order_by(Bill.due_date.asc())
        .all()
    )

    return [
        {"id": r.id, "due_date": str(r.due_date), "amount": float(r.amount), "status": r.status}
        for r in rows
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