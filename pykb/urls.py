from django.conf.urls import url, include

from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^secret$', views.secret_page, name='secret'),
    url(r'^oauth2$', views.oauth2, name='oauth2'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^lo$', views.UserView.as_view(), name='lo'),
    url(r'^$', views.UserView.as_view(), name='index'),
]
