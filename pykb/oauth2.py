import falcon

import json

class OAuth2:
    def __init__(self, **kwargs):
        if 'settings' in kwargs:
            self.settings = kwargs['settings']

    def on_get(self, req, resp, action):
        resp.status = falcon.HTTP_200
        # resp.content_type = 'text/plain'

        if action == 'validate':
            resp.body = '{"V": "OK"}'

        else:
            # By default, return the client parameters to make an auth call.
            resp.body = json.dumps({
                'client_id': self.settings.client_secret['web']['client_id'],
                'project_id': self.settings.client_secret['web']['project_id'],
                'auth_uri': self.settings.client_secret['web']['auth_uri'],
                'token_uri': self.settings.client_secret['web']['token_uri'],
            })
