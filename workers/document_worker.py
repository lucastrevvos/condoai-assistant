import json
import time
from datetime import datetime

from app.core.config import AWS_SQS_QUEUE_URL
from app.infra.sqs import get_sqs_client
from app.infra.s3 import get_s3_client
from app.infra.db import SessionLocal, Base, engine

from app.domain.models import Document
from app.services.extract import extract_text
from app.services.summarize import summarize_text

import httpx
from app.core.config import TELEGRAM_BOT_TOKEN

def send_telegram_message(chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    with httpx.Client(timeout=15) as client:
        client.post(url, json={"chat_id": chat_id, "text": text})



def main():
    if not AWS_SQS_QUEUE_URL:
        raise RuntimeError("AWS_SQS_QUEUE_URL não configurado no .env")

    # garante que DB está inicializado
    Base.metadata.create_all(bind=engine)

    sqs = get_sqs_client()
    s3 = get_s3_client()

    print("📬 Worker rodando. Esperando mensagens...")

    while True:
        resp = sqs.receive_message(
            QueueUrl=AWS_SQS_QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=20,  # long polling
        )

        messages = resp.get("Messages", [])
        if not messages:
            continue

        for msg in messages:
            receipt = msg["ReceiptHandle"]
            body = json.loads(msg["Body"])

            document_id = body.get("document_id")
            if not document_id:
                sqs.delete_message(QueueUrl=AWS_SQS_QUEUE_URL, ReceiptHandle=receipt)
                continue

            db = SessionLocal()
            try:
                doc = db.query(Document).filter(Document.id == document_id).first()
                if not doc:
                    sqs.delete_message(QueueUrl=AWS_SQS_QUEUE_URL, ReceiptHandle=receipt)
                    continue

                doc.status = "processing"
                db.commit()

                # baixar do S3
                obj = s3.get_object(Bucket=doc.bucket, Key=doc.key)
                data = obj["Body"].read()

                # extrair e resumir
                text = extract_text(doc.filename, data)
                summary = summarize_text(text) 

                doc.status = "done"
                doc.summary = summary
                doc.processed_at = datetime.utcnow()
                db.commit()

                # responder no Telegram
                send_telegram_message(
                    doc.chat_id,
                    f"Documento processado: {doc.filename}\n\n{summary}"
                )

                # ack: remove da fila
                sqs.delete_message(QueueUrl=AWS_SQS_QUEUE_URL, ReceiptHandle=receipt)
                print("Processado e removido da fila:", document_id)
            
            except Exception as e:
                try:
                    #tenta registrar erro no DB
                    doc = db.query(Document).filter(Document.id == document_id).first()
                    if doc:
                        doc.status = "error"
                        doc.error = str(e)
                        db.commit()
                finally:
                    # não delete a msg se quiser retry automatico (MVP: delete pra não travar fila)
                    sqs.delete_message(QueueUrl=AWS_SQS_QUEUE_URL, ReceiptHandle=receipt)
                    print("Erro processando:", document_id, str(e))
            finally:
                db.close()

        time.sleep(0.2)


if __name__ == "__main__":
    main()
