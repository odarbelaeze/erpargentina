from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView

from clients.views import *

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url = 'clientes/', permanent = False)),
    url(r'^rutas/$', RouteList.as_view(), name='route-list'),
    url(r'^clientes/$', ClientList.as_view(), name='client-list'),
    url(r'^rutas/(?P<pk>\d+)/$', RouteDetail.as_view(), name='route-detail'),
    url(r'^clientes/(?P<pk>\d+)/$', ClientDetail.as_view(), name='client-detail'),
    url(r'^rutas/(?P<pk>\d+)/add/$', new_client, name='route-client-add'),
)