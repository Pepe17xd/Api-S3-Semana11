import boto3
from util import body,field,fail

def lambda_handler(event,context):
    try:
        bucket=field(body(event),'bucket'); lista=[]
        for pagina in boto3.client('s3').get_paginator('list_objects_v2').paginate(Bucket=bucket):
            lista.extend(o['Key'] for o in pagina.get('Contents',[]))
        return {'statusCode':200,'bucket':bucket,'lista_objetos':lista}
    except Exception as e: return fail(e)
