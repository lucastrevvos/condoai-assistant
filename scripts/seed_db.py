from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.infra.db import Base, engine, SessionLocal
from app.domain.models import Bill

def main():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # evita duplicar seed
        existing = db.query(Bill).count()
        if existing > 0:
            print("Seed já existe. Pulando.")
            return
        
        today = date.today()
        bills = [
            Bill(id="BLT-1001", due_date=today + timedelta(days=2), amount=420.50, status="open"),
            Bill(id="BLT-1002", due_date=today + timedelta(days=5), amount=199.90, status="open"),
        ]
        db.add_all(bills)
        db.commit()
        print("Seed inserido com sucesso")
    finally:
        db.close()


if __name__ == "__main__":
    main()