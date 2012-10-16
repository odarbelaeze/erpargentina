from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView

from stocks.views import *

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url = 'productos/', permanent = False)),
    url(r'^bodegas/$', WareHouseList.as_view(), name='warehouse-list'),
    url(r'^productos/$', ProductList.as_view(), name='product-list'),
    url(r'^bodegas/(?P<pk>\d+)/$', WareHouseDetail.as_view(), name='warehouse-detail'),
    url(r'^productos/(?P<pk>\d+)/$', ProductDetail.as_view(), name='product-detail'),
)