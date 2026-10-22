# api-s3: Guia AWS Academy

## Cambios que debes hacer TU

1. Inicia Learner Lab (Start Lab) y descarga sus credenciales temporales AWS CLI. Configuralas en `~/.aws/credentials` de Linux. No las pongas en el ZIP ni las compartas. Se renuevan cuando el laboratorio reinicia.
2. En Linux, verifica `aws sts get-caller-identity` y `aws iam get-role --role-name LabRole`. Verifica que LabRole y las politicas de Academy permitan S3, Lambda y API Gateway.
3. Dentro de `api-s3/` ejecuta `export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)`. La variable alimenta el ARN en serverless.yml; no copies el ID del profesor.
4. Verifica `serverless --version`. Se elimino `org: geraldocolchado` del archivo original. Si tu version de Serverless exige login/org, usa tu propia cuenta o la version aprobada por el profesor.
5. Despliega con `serverless deploy --stage dev`, `serverless deploy --stage test`, `serverless deploy --stage prod`. Guarda las URL de cada stage. No se han realizado despliegues reales.

## Endpoints

- GET `/s3/lista-buckets` (sin body)
- POST `/s3/bucket/lista-objetos` con `{"bucket":"NOMBRE"}`
- POST `/s3/crear-bucket` con `{"bucket":"NOMBRE-UNICO"}`
- POST `/s3/crear-directorio` con `{"bucket":"NOMBRE","directorio":"evidencias"}`
- POST `/s3/subir-archivo` con `{"bucket":"NOMBRE","directorio":"evidencias","archivo":"prueba.txt","contenido_base64":"SG9sYQ==","content_type":"text/plain"}`

Usa un nombre de bucket S3 globalmente unico en minusculas, distinto por stage (dev/test/prod). S3 representa directorios como prefijos terminados en `/`. La subida acepta Base64 hasta 3 MiB.

## Ejemplo curl para Linux (tambien util para Postman)

Cambia `BASE_URL` por la URL del stage que devuelve el deploy y `BUCKET` por un nombre unico. Repite cambiando ambos para cada stage.

```bash
export BASE_URL='https://TU_ID.execute-api.us-east-1.amazonaws.com/dev'
export BUCKET='taller3-tu-id-unico-dev'
curl -sS "$BASE_URL/s3/lista-buckets"
curl -sS -X POST "$BASE_URL/s3/crear-bucket" -H 'Content-Type: application/json' -d "{\"bucket\":\"$BUCKET\"}"
curl -sS -X POST "$BASE_URL/s3/crear-directorio" -H 'Content-Type: application/json' -d "{\"bucket\":\"$BUCKET\",\"directorio\":\"evidencias\"}"
curl -sS -X POST "$BASE_URL/s3/subir-archivo" -H 'Content-Type: application/json' -d "{\"bucket\":\"$BUCKET\",\"directorio\":\"evidencias\",\"archivo\":\"prueba.txt\",\"contenido_base64\":\"SG9sYQ==\",\"content_type\":\"text/plain\"}"
curl -sS -X POST "$BASE_URL/s3/bucket/lista-objetos" -H 'Content-Type: application/json' -d "{\"bucket\":\"$BUCKET\"}"
```

Para una imagen PNG original, genera JSON desde la carpeta `api-s3`:

```bash
python3 -c 'import json,base64; print(json.dumps({"bucket":"TU_BUCKET","directorio":"evidencias","archivo":"galleta01-small.png","contenido_base64":base64.b64encode(open("../catalogo-productos/imagenes-chicas/galleta01-small.png","rb").read()).decode(),"content_type":"image/png"}))' > payload.json
curl -sS -X POST "$BASE_URL/s3/subir-archivo" -H 'Content-Type: application/json' --data-binary @payload.json
```

## Evidencias para el informe

Captura: despliegues dev/test/prod; pruebas curl; las mismas peticiones en Postman (Body > raw > JSON); Lambda y API Gateway por stage; S3 mostrando bucket, directorio y archivo. Incluye capturas reales en Word/PDF.

## Precauciones

Los endpoints son publicos sin autenticacion (igual que la practica): solo usarlos durante el taller, sin datos sensibles. Los codigos `statusCode` se devuelven en el cuerpo JSON por la integracion Lambda no proxy del profesor; el codigo HTTP externo puede no reflejar el error. AWS Academy puede restringir permisos de crear buckets. No compartas credenciales.
