import uuid
from datetime import datetime, timezone

from app.core.config import AWS_S3_BUCKET
from app.infra.s3 import get_s3_client

def upload_file_to_s3(filename: str, content_type: str, data: bytes) -> dict:
    if not AWS_S3_BUCKET:
        raise RuntimeError("AWS_S3_BUCKET não configurado no .env")
    
    s3 = get_s3_client()

    safe_name = (filename or "file").replace(" ", "_")

    key = f"uploads/{datetime.now(timezone.utc).strftime('%Y/%m/%d')}/{uuid.uuid4()}_{safe_name}"

    s3.put_object(
        Bucket=AWS_S3_BUCKET,
        Key=key,
        Body=data,
        ContentType=content_type or "application/octet-stream"
    )

    return {"bucket": AWS_S3_BUCKET, "key": key}