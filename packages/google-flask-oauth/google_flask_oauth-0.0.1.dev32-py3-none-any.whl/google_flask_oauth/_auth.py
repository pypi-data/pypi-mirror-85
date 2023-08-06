from flask import Flask, request
from .google_oauth import google_oauth
from ._defaults import Defaults
from .decorators import login_required_builder

class AuthWrapper:
  def __init__(self, google_secrets_file_contents, auth_root, login_callback=None, **kwArgs):
    self._google_secrets_file_contents = google_secrets_file_contents
    self._auth_root = auth_root
    self._login_callback = login_callback
    self._kwArgs = kwArgs

    self._auth_app = Flask('google-flask-oauth')
    self._configure_auth_app()

    self._decorators = {
      'login_required': login_required_builder(self._login_callback)
    }

  def _configure_auth_app(self):
    self._auth_app.config.from_object(Defaults)
    self._auth_app.config['AUTH_ROOT'] = self._auth_root
    self._auth_app.config['AUTH_GOOGLE_SA_SECRET_CONTENTS'] = self._google_secrets_file_contents
    for key in self._kwArgs:
      self._auth_app.config['CUSTOM_{}'.format(key.upper())] = self._kwArgs[key]

    self._auth_app.register_blueprint(google_oauth)

  @property
  def auth_app(self):
    return self._auth_app
  
  @property
  def login_required(self):
    return self._decorators['login_required']

def auth(google_secrets_file_contents, auth_root, login_callback=None, **kwArgs):
  return AuthWrapper(google_secrets_file_contents, auth_root, login_callback=login_callback, **kwArgs)

def aws_auth(login_callback=None, **kwArgs):
  from ._aws_bootstrap import GOOGLE_CLIENT_SECRET, AUTH_ROOT
  return auth(GOOGLE_CLIENT_SECRET, AUTH_ROOT, login_callback=login_callback, **kwArgs)
