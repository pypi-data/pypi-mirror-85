import os
import boto3
import json

_client = boto3.client('secretsmanager')
_secretname = os.getenv('OAUTH_CLIENT_SECRET_ID')

if _secretname:
  record = _client.get_secret_value(SecretId=_secretname)
  config = json.loads(record['SecretString'])

  GOOGLE_CLIENT_SECRET = config['google_client_config']
  AUTH_ROOT = os.getenv('AUTH_ROOT_OVERRIDE') or config['auth_root']
else:
  GOOGLE_CLIENT_SECRET = ""
  AUTH_ROOT = ""