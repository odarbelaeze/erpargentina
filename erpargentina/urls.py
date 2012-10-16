from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

# Home class view
from stocks.views import Index as Home

urlpatterns = patterns('',
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Home.as_view()),
    url(r'^login/$', 'django.contrib.auth.views.login', name = "login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name = "logout"),
)

urlpatterns += patterns('',
    url(r'^inventario/', include('stocks.urls')),
)

urlpatterns += patterns('',
    url(r'^clientes/', include('clients.urls')),
)