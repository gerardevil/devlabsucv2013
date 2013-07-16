from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'principal.views.inicio', name='home'),
	#url(r'^assets/$', 'principal.views.getRecurso'),
    # url(r'^$', 'programacion_docente.views.home', name='home'),
    # url(r'^programacion_docente/', include('programacion_docente.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
