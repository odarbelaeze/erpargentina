from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView

from stocks.views import WareHouseList
from stocks.views import ProductList
from stocks.views import PriceTagList
from stocks.views import StockList
from stocks.views import StockEventList
from stocks.views import WareHouseDetail
from stocks.views import ProductDetail
from stocks.views import PriceTagDetail
from stocks.views import StockDetail
from stocks.views import StockEventDetail

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url = 'product-list')),
    url(r'^bodegas/$', WareHouseList.as_view(), name='warehouse-list'),
    url(r'^productos/$', ProductList.as_view(), name='product-list'),
    url(r'^precios/$', PriceTagList.as_view(), name='pricetag-list'),
    url(r'^existencias/$', StockList.as_view(), name='stock-list'),
    url(r'^regexistencias/$', StockEventList.as_view(), name='stockevent-list'),
    url(r'^bodegas/(?P<pk>\d+)/$', WareHouseDetail.as_view(), name='warehouse-detail'),
    url(r'^productos/(?P<pk>\d+)/$', ProductDetail.as_view(), name='product-detail'),
    url(r'^precios/(?P<pk>\d+)/$', PriceTagDetail .as_view(), name='pricetag-detail'),
    url(r'^existencias/(?P<pk>\d+)/$', StockDetail.as_view(), name='stock-detail'),
    url(r'^regexistencias/(?P<pk>\d+)/$', StockEventDetail.as_view(), name='stockevent-detail'),
)