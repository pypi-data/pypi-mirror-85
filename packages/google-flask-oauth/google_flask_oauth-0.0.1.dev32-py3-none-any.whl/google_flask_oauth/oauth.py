from flask import Blueprint, request, jsonify, current_app
from google_auth_oauthlib.flow import Flow
from base64 import urlsafe_b64encode
import json

oauth = Blueprint('oauth', __name__)

def build_flow(state=None):
  flow = Flow.from_client_config(
    current_app.config['AUTH_SA_SECRET_CONTENTS'],
    ['openid', 'https://www.googleapis.com/auth/userinfo.email'],
    state=state
  )
  flow.redirect_uri = f'https://{current_app.config["AUTH_ROOT"]}/oauth/token'
  return flow

@oauth.route('/oauth/start', methods=['POST'])
def oauth_start():
  flow = build_flow()
  authorization_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
  return jsonify({
    'redirect_url': authorization_url
  }), 200

@oauth.route('/oauth/exchange', methods=['POST'])
def oauth_exchange():
  req_data = request.get_json(force=True)
  code = req_data.get('code', '')
  state = req_data.get('state', '')
  if not code:
    return jsonify({'error': 'Must provide authorization code'}), 400
  if not state:
    return jsonify({'error': 'Must provide state'}), 400
  flow = build_flow(state)
  flow.fetch_token(code=code)
  credentials = flow.credentials
  session = flow.authorized_session()
  profile_info = session.get('https://www.googleapis.com/userinfo/v2/me').json()

  assembled_credentials = {
    'token': credentials.token,
    'refresh_token': credentials.refresh_token,
    'username': profile_info['email'],
    'userid': profile_info['id'],
    'picture': profile_info.get('picture', '')
  }
  current_app.logger.info(f'Assembled credentials: {json.dumps(assembled_credentials)}')
  return jsonify(assembled_credentials), 200
