from django.conf.urls import patterns, include, url
from django.contrib import admin
from configuracion import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'principal.views.inicio', name='home'), 
    url(r'^login$', 'principal.views.loginUser', name='login'),
    url(r'^logout$', 'principal.views.logoutUser', name='log'),
    url(r'^profile$', 'principal.views.profile', name='profile'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #Generic views:
    url(r'^admins$', 'principal.views.admins', name='administrador'),
    url(r'^admins/modelos$', 'principal.views.listarm', name='listado_modelos'), #Lista de todos los modelos
    url(r'^admins/modelos/(?P<modelo>[^/]+)$', 'principal.views.listar', name='listar_modelo'), #Lista de todos los objetos del modelo    url(r'^admins/modelos/(?P<modelo>[^/]+)/crear/$', 'principal.views.insertar', name='insertar'), #Inserta un objeto
    url(r'^admins/modelos/(?P<modelo>[^/]+)/borrar/(?P<key>\d+)$', 'principal.views.borrar', name='borrar'), #Borra un objeto
    url(r'^admins/modelos/(?P<modelo>[^/]+)/editar/(?P<key>\d+)$', 'principal.views.editar', name='editar'), #Edita un objeto
    url(r'^admins/modelos/(?P<modelo>[^/]+)/(?P<key>\d+)$', 'principal.views.leer', name='leer'), #Muestra todos los atributos de un objeto
    url(r'^admins/modelos/(?P<modelo>[^/]+)/crear$', 'principal.views.insertar', name='insertar'), # Permite insertar un Objeto

    url(r'^horario$', 'principal.views.horario', name='horario'),
    url(r'^schedulexrequest/(?P<rol>[^/]+)$', 'principal.views.getScheduleByRequest', name='schedulexrequest'),
    url(r'^subjectxrequest$', 'principal.views.getSubjectByRequest', name='subjectxrequest'),
    url(r'^userxcenter$', 'principal.views.getUserByCenter', name='userxcenter'),
    
    #Agregar Materia
    #url(r'^horarios_materia/(?P<key>\d+)$', 'principal.views.horarios_materia', name='horarios'), #Devuelve los horarios de una materia
    url(r'^horarios_materia$', 'principal.views.horarios_materia', name='horarios'), #Devuelve los horarios de una materia

    #URLs para templates sin backend
    url(r'^profile/editar$', 'principal.views.editar_profesor', name='horarios'),

)

'''
Allow development static files 
'''

if settings.DEBUG:
    urlpatterns += patterns('',
             (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS, 'show_indexes':True}),
         )