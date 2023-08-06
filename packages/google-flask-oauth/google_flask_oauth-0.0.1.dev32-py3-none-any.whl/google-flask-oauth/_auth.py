from flask import Flask, request
from .oauth import oauth
from ._defaults import Defaults

def auth(secrets_file_contents, domain, **kwArgs):
  auth_app = Flask('google-flask-oauth')
  auth_app.config.from_object(Defaults)
  auth_app.config['AUTH_ROOT_DOMAIN'] = domain
  auth_app.config['AUTH_SA_SECRET_CONTENTS'] = secrets_file_contents
  for key in kwArgs:
    auth_app.config['CUSTOM_{}'.format(key.upper())] = kwArgs[key]

  auth_app.register_blueprint(oauth)

  return auth_app

def aws_auth(**kwArgs):
  from ._aws_bootstrap import CLIENT_SECRET, DOMAIN
  return auth(CLIENT_SECRET, DOMAIN, **kwArgs)
