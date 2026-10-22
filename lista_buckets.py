import boto3
from util import fail

def lambda_handler(event,context):
    try: return {'statusCode':200,'lista_buckets':[b['Name'] for b in boto3.client('s3').list_buckets().get('Buckets',[])]}
    except Exception as e: return fail(e)
