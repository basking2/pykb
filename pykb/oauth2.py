import falcon

import json
import requests
from jose import jwt

class OAuth2:
    def __init__(self, **kwargs):
        if 'settings' in kwargs:
            self.settings = kwargs['settings']

        self.state = "FIXME - this should be random."

    def on_get(self, req, resp, action):
        resp.status = falcon.HTTP_200
        # resp.content_type = 'text/plain'

        if 'code' in req.params:
            # Get and validate a token.
            code = req.params['code']
            if 'state' in req.params:
                state = req.params['state']
            else:
                state = 'no state provided'

            # FIXME - validate state.

            (token, success) = self.validate_code(code, self.settings.client_secret)

            if success:
                resp.body = json.dumps({'token': token})
            else:
                resp.body = json.dumps({'error': token})

        else:
            # By default, return the client parameters to make an auth call.
            resp.body = json.dumps({
                'client_id': self.settings.client_secret['web']['client_id'],
                'project_id': self.settings.client_secret['web']['project_id'],
                'auth_uri': self.settings.client_secret['web']['auth_uri'],
                'token_uri': self.settings.client_secret['web']['token_uri'],
                'state': self.state,
            })

    @staticmethod
    def validate_code(code, client_secret):
        '''
        Fetch and validate an access ticket given a code and the contents of client_secret.json.

        This returns (string, False) on an error.
        This reteurns (token, True) on success.
        '''
        options = {
            'client_id': client_secret['web']['client_id'],
            'client_secret': client_secret['web']['client_secret'],
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost:8000/login',
        }

        resp = requests.post(client_secret['web']['token_uri'], options)

        # We got the web token!
        token_json = resp.json()

        if 'error' in token_json:
            msg = token_json['error_description']
            err = token_json['error']
            return (msg, False)
        else:
            certs = requests.get(client_secret['web']['auth_provider_x509_cert_url']).json()
            # Validate the JWT.
            id_token = jwt.decode(
                token_json['id_token'],
                certs,
                options = {
                    'verify_aud': False,
                    'verify_iat': False,
                    'verify_exp': False,
                    'verify_nbf': False,
                    'verify_iss': False,
                    'verify_sub': False,
                    'verify_jti': False,
                },
                access_token=token_json['access_token'])

            return (token_json['access_token'], True)
