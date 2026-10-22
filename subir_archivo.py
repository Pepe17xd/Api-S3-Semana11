import boto3,base64,binascii
from util import body,field,path,fail

def lambda_handler(event,context):
    try:
        data=body(event); bucket=field(data,'bucket'); directorio=path(field(data,'directorio')); archivo=path(field(data,'archivo'))
        if '/' in archivo: raise ValueError('archivo debe ser un nombre, sin /')
        try: contenido=base64.b64decode(field(data,'contenido_base64'),validate=True)
        except (binascii.Error,ValueError): raise ValueError('Base64 invalido')
        if len(contenido)>3*1024*1024: raise ValueError('Archivo mayor a 3 MiB')
        tipo=data.get('content_type','application/octet-stream')
        if not isinstance(tipo,str) or not tipo: raise ValueError('content_type invalido')
        clave=f'{directorio}/{archivo}'
        boto3.client('s3').put_object(Bucket=bucket,Key=clave,Body=contenido,ContentType=tipo)
        return {'statusCode':201,'mensaje':'Archivo subido','bucket':bucket,'key':clave,'bytes':len(contenido)}
    except Exception as e: return fail(e)
