import falcon

from pykb.pykb import PyKb

app = falcon.API()

app.add_route('/pykb', PyKb())
