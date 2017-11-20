import falcon

class OAuth2:
    def __init__(self, **kwargs):
        if 'settings' in kwargs:
            self.settings = kwargs['settings']

    def on_get(self, req, resp, action):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/plain'
        resp.body = ("Lorem " "Ipsum. " + str(action))
