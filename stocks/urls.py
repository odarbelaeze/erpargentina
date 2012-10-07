from django.conf.urls import patterns, url

from stocks.views import ProductList

urlpatterns = patterns('',
    url(r'^$', ProductList.as_view(), name='product-list'),
)