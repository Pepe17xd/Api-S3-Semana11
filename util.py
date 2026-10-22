import json
from botocore.exceptions import ClientError

def body(event):
    data=(event or {}).get('body',{})
    if isinstance(data,str):
        try: data=json.loads(data)
        except ValueError: raise ValueError('JSON invalido')
    if not isinstance(data,dict): raise ValueError('Body debe ser JSON objeto')
    return data

def field(data,key):
    v=data.get(key)
    if not isinstance(v,str) or not v.strip(): raise ValueError(f'Falta {key}')
    return v.strip()

def path(v):
    v=v.strip('/')
    if not v or '\\' in v or '\x00' in v or any(x in ('.','..') for x in v.split('/')): raise ValueError('Ruta invalida')
    return v

def fail(e):
    if isinstance(e,ValueError): return {'statusCode':400,'error':str(e)}
    if isinstance(e,ClientError): return {'statusCode':e.response.get('ResponseMetadata',{}).get('HTTPStatusCode',500),'error':e.response.get('Error',{}).get('Code','S3Error')}
    return {'statusCode':500,'error':'Error interno'}
