from django.shortcuts import render

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.contrib.auth import login
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.http import urlencode
from django.views.generic.base import TemplateView
import json
import requests
from jose import jwt


from django.contrib.auth.models import User

client_json = json.loads(open('client_secret.json').read())

anti_forgery_token = "some random value - fix me."

class UserView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated()
        if 'oauth_login_token' in self.request.session:
            context['oauth_login_token'] = self.request.session['oauth_login_token']
        if 'oauth_id_token' in self.request.session:
            context['oauth_id_token'] = self.request.session['oauth_id_token']
        return context

    def get_template_names(self):
        t = self.request.path.split('/')[-1]
        if t == '':
            t = 'index.html'
        else:
            t = t + ".html"
        return [t]

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

    if 'error' in token_json:
        msg = token_json['error_description']
        err = token_json['error']
        t = get_template('oauth2_error.html')
        html = t.render({
            'msg': msg,
            'err': err,
        })
        return HttpResponse(html, status=400)

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

    try:
        user = User.objects.get(email=id_token['email'])
    except User.DoesNotExist as e:
        user = User.objects.create_user(id_token['email'], id_token['email'])
        user.save()

    login(request, user)

    t = get_template("oauth2.html")
    html = t.render({
        'scope': scope,
        'token_json': str(token_json),
        'id_token': str(id_token),
    })
    return HttpResponse(html, status=200)

def logout_view(request):
    logout(request)
    # Return an HttpResponseRedirect.
    return redirect(reverse('index'))

def login_view(request):
    t = get_template('login.html')
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
    html = t.render({
        'gauth': gauth,
    })
    return HttpResponse(html)

@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)
