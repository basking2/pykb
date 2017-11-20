import falcon

class PyKb():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/plain'
        resp.body = ("Lorem" "Ipsum.")
