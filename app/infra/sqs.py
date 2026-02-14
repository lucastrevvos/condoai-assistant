import boto3
from app.core.config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

def get_sqs_client():
    kwargs = {}
    if AWS_REGION:
        kwargs["region_name"] = AWS_REGION
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

    return boto3.client("sqs", **kwargs)