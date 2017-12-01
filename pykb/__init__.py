import falcon

import pykbdb

from pykb.settings import Settings
from pykb.pykb import PyKb
# from pykb.oauth2 import OAuth2
from pykb.oauth2 import OAuth2

app = falcon.API()

settings = Settings()

print(pykbdb.engine)

app.add_route('/pykb', PyKb(settings = settings))
app.add_route('/oauth2/{action}', OAuth2(settings = settings))
