# How to read and write blobs.

import falcon
import json
import pykbdb
import re
import datetime
from pykb.oauth2 import OAuth2
from pykb.validators import AuthorizationValidator
from pykb.validators import RoleValidator

import pykbdb

def convert_blob_to_map(blob):
    return {
        'id': blob.id,
        'title': blob.title,
        'tags': list(blob.gettags())
    }

class Blobs():
    def __init__(self, **kwargs):
        if 'settings' in kwargs:
            self.settings = kwargs['settings']

    @falcon.before(AuthorizationValidator())
    @falcon.before(RoleValidator("blobs"))
    def on_get(self, req, resp, **kwargs):
        sess = pykbdb.Session()
        try:
            if 'id' in kwargs:
                id = kwargs['id']
                blobs = [ sess.query(pykbdb.Blob).get(id) ]
            else:
                blobs = sess.query(pykbdb.Blob).all()

            resp.status = falcon.HTTP_200
            resp.content_type = 'application/json'
            resp.body = json.dumps({ "text": "OK" , 'blobs': [ convert_blob_to_map(x) for x in blobs ] })
        finally:
            sess.close()
