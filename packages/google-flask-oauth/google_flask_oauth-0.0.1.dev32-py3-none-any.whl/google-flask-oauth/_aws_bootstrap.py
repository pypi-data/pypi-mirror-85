import os
import boto3
import json

_client = boto3.client('secretsmanager')
_secretname = os.getenv('OAUTH_CLIENT_SECRET_ID')

if _secretname:
  record = _client.get_secret_value(SecretId=_secretname)
  config = json.loads(record['SecretString'])

  CLIENT_SECRET = config['client_secret']
  DOMAIN = config['domain']
else:
  CLIENT_SECRET = ""
  DOMAIN = ""