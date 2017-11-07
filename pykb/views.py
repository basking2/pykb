from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse

from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.template.loader import get_template

def index(request):
    t = get_template('index.html')
    h = t.render({"var": "val"})
    return HttpResponse(h)

class ApiEndpoint(ProtectedResourceView):
    def get(request):
        return HttpResponse("Hullo, world.")

@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)
