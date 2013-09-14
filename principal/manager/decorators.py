#decorators.py

############################
# Custom Decorators bellow #
############################


from django.db import models
from django.contrib.auth.models import User
from django.db.models import get_app, get_models, get_model
from django.http import Http404
from principal.models import *

def validateInputCrudData(view):
	def wrapper(request, modelo, key=None):
		if modelo in map((lambda model : model._meta.verbose_name),get_models(get_app('principal'))):
			if key is not None and key != '':
				if key in map((lambda row: str(row.pk)),get_model('principal',str(modelo).replace(' ','')).objects.all()):
					return view(request, modelo, key)
				else:
					raise Http404
			else:	
				return view(request, modelo)
		else:
			raise Http404
	return wrapper


def coordinatorRequired(view):
	def wrapper(request,rol):
		try:
			roles = UsuarioRol.objects.filter(cedula__usuario_id__pk = request.user.pk).values('rol')
			exclusive_id_rol = [e['rol'] for e in roles]
			str_roles = Rol.objects.filter(pk__in=exclusive_id_rol).values('rol_id')
			if {'rol_id':u'CC'} in str_roles:
				return view(request,rol)	
			else:				
				raise Http404
		except Exception, e:
			raise Http404
	return wrapper