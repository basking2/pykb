# How to read and write blobs.

import falcon
import json
import pykbdb
import re
import datetime
from pykb.oauth2 import OAuth2
from pykb.validators import AuthorizationValidator
from pykb.validators import RoleValidator

class Blobs():
    def __init__(self, **kwargs):
        if 'settings' in kwargs:
            self.settings = kwargs['settings']

    @falcon.before(AuthorizationValidator())
    @falcon.before(RoleValidator("blobs"))
    def on_get(self, req, resp, **kwargs):
        # (msg, success) = OAuth2.validate_session(req)
        # print("MSG", msg)
        # print("SUCC", success)

        print("IN GET BLOBS")

        if 'id' in kwargs:
            id = kwargs['id']
        else:
            id = None

        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        resp.body = json.dumps({ "text": "OK" })
