import json
import time
from datetime import datetime

from app.infra.sqs import get_sqs_client
from app.core.config import AWS_SQS_QUEUE_URL
from app.infra.db import SessionLocal, Base, engine
from app.domain.models import Bill  # só pra garantir que models carregam; vamos criar table de docs no passo seguinte

# TODO no próximo passo: criar model Document e salvar resultado nele


def main():
    if not AWS_SQS_QUEUE_URL:
        raise RuntimeError("AWS_SQS_QUEUE_URL não configurado no .env")

    # garante que DB está inicializado
    Base.metadata.create_all(bind=engine)

    sqs = get_sqs_client()
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

            print("✅ Job recebido:", body)

            # PROCESSAMENTO (MVP)
            # aqui no próximo passo vamos baixar do S3 e extrair texto / resumir com LLM
            processed_at = datetime.utcnow().isoformat()
            print("🛠️ Processado em:", processed_at)

            # deletar msg da fila (ack)
            sqs.delete_message(QueueUrl=AWS_SQS_QUEUE_URL, ReceiptHandle=receipt)
            print("🧹 Job removido da fila")

        time.sleep(0.2)


if __name__ == "__main__":
    main()
