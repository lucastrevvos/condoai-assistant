from app.services.tools import get_upcoming_bills, format_bills_message

class FinanceAgent:
    def handle(self, text: str) -> str: 
        # v1: sempre retorna boletos próximos
        bills = get_upcoming_bills(days=7)
        return format_bills_message(bills)