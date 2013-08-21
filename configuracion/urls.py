from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	url(r'^$', 'principal.views.inicio', name='home'), 
	url(r'^login$', 'principal.views.login', name='login'),
    url(r'^profile$', 'principal.views.profile', name='profile'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^listarMaterias$', 'principal.views.listarMaterias', name='listarMaterias'),
	url(r'^obtenerMateria$', 'principal.views.obtenerMateria', name='obtenerMateria'),
	url(r'^guardarMateria$', 'principal.views.guardarMateria', name='guardarMateria'),
	url(r'^eliminarMateria$', 'principal.views.eliminarMateria', name='eliminarMateria'),

    url(r'^admins$', 'principal.views.admins', name='administrador'),
    url(r'^admins/modelos$', 'principal.views.listarm', name='listado_modelos'), #Lista de todos los modelos

    url(r'^admins/modelos/(?P<modelo>[^/]+)$', 'principal.views.listar', name='listar_modelo'), #Lista de todos los objetos del modelo
    url(r'^admins/modelos/(?P<modelo>[^/]+)/crear/$', 'principal.views.insertar', name='insertar'), #Inserta un objeto
    url(r'^admins/modelos/(?P<modelo>[^/]+)/borrar/(?P<key>\d+)$', 'principal.views.borrar', name='borrar'), #Borra un objeto
    url(r'^admins/modelos/(?P<modelo>[^/]+)/editar/(?P<key>\d+)$', 'principal.views.editar', name='editar'), #Edita un objeto
    url(r'^admins/modelos/(?P<modelo>[^/]+)/(?P<key>\d+)$', 'principal.views.leer', name='leer'), #Muestra todos los atributos de un objeto
    #url(r'^admins/modelos/aula/crear/$', 'principal.views.insertarAula', name='insertarAula'),
    #url(r'^listarAulas/$', 'principal.views.listarAulas', name='listarAulass'),
    #url(r'^admins/modelos/aula/editar/(?P<aula_id>\d+)$', 'principal.views.editarAula', name='editarAula'),
    #url(r'^admins/modelos/aula/borrar/(?P<aula_id>\d+)$', 'principal.views.borrarAula', name='borrarAula'),
    url(r'^admins/modelos/aula/borrar/(?P<aula_id>\d+)$', 'principal.views.borrarAula', name='borrarAula'),
	url(r'^ppalCrudMaterias$', 'principal.views.ppalCrudMaterias', name='ppalCrudMaterias'),
	url(r'^crearMateria$', 'principal.views.crearMateria', name='crearMateria'),
	url(r'^modificarMateria$', 'principal.views.modificarMateria', name='modificiarMateria'),



)
