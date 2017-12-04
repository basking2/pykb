import json

import datetime

class Settings:
    session_expiration = datetime.timedelta(seconds = 60 * 60)
    with open('client_secret.json') as io:
        client_secret = json.load(io)
