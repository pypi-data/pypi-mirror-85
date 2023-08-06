from flask import Blueprint, request, jsonify
from google_auth_oauthlib.flow import Flow

oauth = Blueprint('oauth', __name__)

@oauth.route('/oauth/start', methods=['GET'])
def oauth_start():
  flow = Flow.from_client_config(
    auth_app.config['AUTH_SA_SECRET_CONTENTS'],
    ['https://www.googleapis.com/auth/userinfo.email']
  )
  flow.redirect_uri = f'https://{auth_app.config['AUTH_ROOT_DOMAIN']}/auth/oauth/exchange'
  authorization_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
  return jsonify({
    'redirect_url': authorization_url
  }), 200

@oauth.route('/oauth/exchange', method=['POST'])
def oauth_exchange():
  pass
