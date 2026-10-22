import boto3
from util import body,field,path,fail

def lambda_handler(event,context):
    try:
        data=body(event); bucket=field(data,'bucket'); directorio=path(field(data,'directorio'))+'/'
        boto3.client('s3').put_object(Bucket=bucket,Key=directorio,Body=b'')
        return {'statusCode':201,'mensaje':'Directorio creado','bucket':bucket,'directorio':directorio}
    except Exception as e: return fail(e)
