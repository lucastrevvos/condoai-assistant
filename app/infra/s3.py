import boto3
from app.core.config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY 

def get_s3_client():
    return boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID or None,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY  or None
    )