from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse

from django.http import HttpResponse
from django.template.loader import get_template

from django.utils.http import urlencode
import json
import requests
from jose import jwt

client_json = json.loads(open('client_secret.json').read())

anti_forgery_token = "some random value - fix me."

def index(request):
    t = get_template('index.html')
    client_id = client_json['web']['client_id']
    auth_uri = client_json['web']['auth_uri']
    q = urlencode({
        'scope': ' '.join(['profile', 'email', 'openid']),
        'client_id': client_id,
        'access_type': 'offline',
        'include_granted_scopes': 'true',
        'state': anti_forgery_token,
        'redirect_uri': 'http://localhost:8000/oauth2',
        'response_type': 'code',
        })

    gauth = auth_uri + "?" + q

    login_val = 'nothing'

    if 'oauth_login_token' in request.session:
        login_val = str(request.session['oauth_login_token']) + \
        "\n\n" 

    if 'oauth_id_token' in request.session:
        login_val += str(request.session['oauth_id_token'])

    h = t.render({
        "var": "val",
        "auth": request.user.is_authenticated(),
        "gauth": gauth,
        'login': login_val,
    })

    return HttpResponse(h)

def oauth2(request):
    '''
    Handle OAuth2 responses.

    Specifically, after the initial concent page this goes to the grant, then the access token.
    '''
    s = "ok\n"
    s += str(request.session)+"\n"
    for k in request.GET:
        s += k +" = "+request.GET[k]+"\n"

    # Check that this request was not forged in some way.
    if anti_forgery_token != request.GET['state']:
        raise Exception("State did not match!")

    # Fetch the scope we would like to get a token for.
    scope = ''
    for k in request.GET['scope'].split(' '):
        if (k.endswith('plus.me')):
            scope = k

    options = {
        'client_id': client_json['web']['client_id'],
        'client_secret': client_json['web']['client_secret'],
        'grant_type': 'authorization_code',
        'code': request.GET['code'],
        'redirect_uri': 'http://localhost:8000/oauth2',
    }

    resp = requests.post(client_json['web']['token_uri'], options)

    # We got the web token!
    token_json = resp.json()

    # Get the Google Certificates.
    certs = requests.get(client_json['web']['auth_provider_x509_cert_url']).json()

    # Validate the JWT.
    id_token = jwt.decode(
        token_json['id_token'],
        certs,
        options = {
            'verify_aud': False,
            'verify_iat': False,
            'verify_exp': False,
            'verify_nbf': False,
            'verify_iss': False,
            'verify_sub': False,
            'verify_jti': False,
        },
        access_token=token_json['access_token']
    )


    request.session['oauth_login_token'] = token_json
    request.session['oauth_id_token'] = id_token

    # access_token
    # expires_in
    # token_type
    # id_token

    s += "\n\nSCOPE "+scope +"\n"
    s += "\n\n"+str(token_json)+"\n\n"
    s += "\n\n"+str(id_token)+"\n\n"
    return HttpResponse(s, content_type="text/plain", status=200)

@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)
