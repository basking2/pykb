from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse

from django.http import HttpResponse
from django.template.loader import get_template

from django.utils.http import urlencode
import json
import requests

client_json = json.loads(open('client_secret.json').read())

def index(request):
    t = get_template('index.html')
    client_id = client_json['web']['client_id']
    auth_uri = client_json['web']['auth_uri']
    q = urlencode({
        'scope': ' '.join(['profile', 'email', 'openid']),
        'client_id': client_id,
        'access_type': 'offline',
        'include_granted_scopes': 'true',
        'state': 'state_parameter_passthrough_value',
        'redirect_uri': 'http://localhost:8000/oauth2',
        'response_type': 'code',
        })

    gauth = auth_uri + "?" + q

    h = t.render({
        "var": "val",
        "auth": request.user.is_authenticated(),
        "gauth": gauth,
    })

    return HttpResponse(h)

def oauth2(request):
    '''
    Handle OAuth2 responses.
    '''
    # [08/Nov/2017 06:45:24] "GET /oauth2?state=state_parameter_passthrough_value&code=4/.AACprXXVO83VW4M94kxFcJH2WeXa8oKORrFscML2x072Ibz6lRpap6F_w4_WRhHcOJVemJyNYSO2oo-JWTFSbHM&scope=https://www.googleapis.com/auth/userinfo.profile+https://www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/plus.me&authuser=0&session_state=518c501ce49002a28c88bac3d317f619f5ae7e8c..eed6&prompt=consent HTTP/1.1" 404 2560
    s = "ok\n"
    s += str(request.session)+"\n"
    for k in request.GET:
        s += k +" = "+request.GET[k]+"\n"

    scope = ''
    for k in request.GET['scope'].split(' '):
        if (k.endswith('plus.me')):
            scope = k

    client_id = client_json['web']['client_id']
    client_secret = client_json['web']['client_secret']

    token_uri = client_json['web']['token_uri']

    options = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': request.GET['code'],
        'redirect_uri': 'http://localhost:8000/oauth2',
    }

    resp = requests.post(token_uri, options)

    token_json = resp.json()

    # access_token
    # expires_in
    # token_type
    # id_token

    s += "\n\nSCOPE "+scope +"\n"
    s += "\n\n"+str(token_json)+"\n\n"
    return HttpResponse(s, content_type="text/plain", status=200)

@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)
