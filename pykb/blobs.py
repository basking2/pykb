# How to read and write blobs.

import falcon
import json
import pykbdb
import re
import datetime

class Blobs():
    def __init__(self, **kwargs):
        if 'settings' in kwargs:
            self.settings = kwargs['settings']

    def on_get(self, req, resp, **kwargs):
        print("IN GET BLOBS")

        if 'id' in kwargs:
            id = kwargs['id']
        else:
            id = None

        authorization = req.get_header('Authorization', False, '')
        m = re.compile('^\s*bearer\s+(.*)$', re.IGNORECASE).\
            match(authorization)
        if m:
            session = pykbdb.Session()
            websessions = session.query(pykbdb.WebSession).filter(pykbdb.WebSession.authorization == m[1])
            if websessions.count() > 0:
                now = datetime.datetime.now()
                if websessions[0].expiration < now:
                    session.query(pykbdb.WebSession).filter(pykbdb.WebSession.expiration < now).delete()
                    session.commit()
                    print("GOT EXPIRED WS")
                else:
                    print("GOT WS")
            else:
                print("GOT NO WS")
            session.close()

        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        resp.body = json.dumps({ "text": "OK" })
