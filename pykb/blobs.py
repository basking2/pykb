# How to read and write blobs.

import falcon
import json

class Blobs():
    def __init__(self, **kwargs):
        if 'settings' in kwargs:
            self.settings = kwargs['settings']

    def on_get(self, req, resp):
        print("IN GET BLOBS")
        if 'Authorization' in req.headers:
            print("AUTHRIZATION: "+req.headers['Authorization'])


        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        resp.body = json.dumps({ "text": "OK" })
