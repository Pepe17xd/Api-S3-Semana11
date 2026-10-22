import boto3
from util import body,field,fail

def lambda_handler(event,context):
    try:
        bucket=field(body(event),'bucket')
        boto3.client('s3').create_bucket(Bucket=bucket)
        return {'statusCode':201,'mensaje':'Bucket creado','bucket':bucket}
    except Exception as e: return fail(e)
