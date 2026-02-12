from app.services.tools import get_upcoming_bills, format_bills_message
from sqlalchemy.orm import Session

class FinanceAgent:
    def handle(self, text: str, db: Session) -> str: 

        bills = get_upcoming_bills(db=db, days=7)
        return format_bills_message(bills)