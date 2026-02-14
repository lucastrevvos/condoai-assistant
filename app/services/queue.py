import json
from app.core.config import AWS_SQS_QUEUE_URL
from app.infra.sqs import get_sqs_client

def enqueue_document_job(payload: dict) -> dict:
    if not AWS_SQS_QUEUE_URL:
        raise RuntimeError("AWS_SQS_QUEUE_URL não configurado no .env")
    
    sqs = get_sqs_client()
    
    resp = sqs.send_message(
        QueueUrl=AWS_SQS_QUEUE_URL,
        MessageBody=json.dumps(payload)
    )

    return {"message_id": resp.get("MessageId")}