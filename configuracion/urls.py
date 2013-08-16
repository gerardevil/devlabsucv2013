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
    url(r'^admins/modelos$', 'principal.views.listarm', name='listado_modelos'),
    url(r'^admins/modelos/(?P<modelo>[^/]+)$', 'principal.views.datos', name='listar_modelo'),
    # url(r'^listarUsuarios/$', 'principal.views.listarUsuarios', name='listarUsuarios'),
    url(r'^admins/modelos/usuario/crear/$', 'principal.views.insertarUsuario', name='insertarUsuario'),
    url(r'^admins/modelos/usuario/borrar/(?P<usuario_id>\d+)$', 'principal.views.borrarUsuario', name='borrarUsuario'),
    url(r'^admins/modelos/usuario/editar/(?P<usuario_id>\d+)$', 'principal.views.editarUsuario', name='editarUsuario'),
    url(r'^admins/modelos/aula/crear/$', 'principal.views.insertarAula', name='insertarAula'),
    url(r'^listarAulas/$', 'principal.views.listarAulas', name='listarAulass'),
    url(r'^admins/modelos/aula/editar/(?P<aula_id>\d+)$', 'principal.views.editarAula', name='editarAula'),
    url(r'^admins/modelos/aula/borrar/(?P<aula_id>\d+)$', 'principal.views.borrarAula', name='borrarAula'),

)
