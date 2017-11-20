import falcon

from pykb.settings import Settings
from pykb.pykb import PyKb

app = falcon.API()

settings = Settings()

app.add_route('/pykb', PyKb(settings = settings))
