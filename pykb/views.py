from django.shortcuts import render

from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hullo, world.")

class ApiEndpoint(ProtectedResourceView):
    def get(request):
        return HttpResponse("Hullo, world.")
