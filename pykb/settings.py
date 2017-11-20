import json

class Settings:
    with open('client_secret.json') as io:
        client_secret = json.load(io)
