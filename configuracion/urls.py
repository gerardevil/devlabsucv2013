from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	url(r'^$', 'principal.views.inicio', name='home'), 
	url(r'^login$', 'principal.views.login', name='login'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls))
)
