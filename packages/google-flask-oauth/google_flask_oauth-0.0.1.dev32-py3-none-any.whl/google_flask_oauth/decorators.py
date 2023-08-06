from functools import wraps
import re
from flask import request, current_app, Response, g
from google.oauth2.credentials import Credentials
import google
import requests

def login_required_builder(login_callback=None):
  def login_required(f):
    @wraps(f)
    def wrap(*args, **kwArgs):
      def failit():
        resp = Response()
        resp.headers['WWW-Authenticate'] = 'Bearer'
        resp.status_code = 401
        return resp

      if not request.headers['authorization']:
        return failit()
      matcher = re.match(r'(?i)bearer (.*)$', request.headers['authorization'])
      if not matcher:
        return failit()

      token = matcher.group(1)
      query_params = {'access_token': token}
      r = requests.post('https://oauth2.googleapis.com/tokeninfo', params=query_params)

      if r.status_code != requests.codes.ok:
        return failit()
      
      g.email = r.json()['email']
      if login_callback:
        g.user_data = login_callback(g.email)

      return f(*args, **kwArgs)

    return wrap
  return login_required