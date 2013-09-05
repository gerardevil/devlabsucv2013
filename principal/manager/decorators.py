#decorators.py

############################
# Custom Decorators bellow #
############################

from principal.models import *
from django.db import models
from django.contrib.auth.models import User
from django.db.models import get_app, get_models, get_model
from django.shortcuts import render_to_response

def validateInputCrudData(view):
	def wrapper(request, modelo, key=None):
		if modelo in map((lambda model : model._meta.verbose_name),get_models(get_app('principal'))):
			if key is not None and key != '':
				if key in map((lambda row: str(row.pk)),get_model('principal',str(modelo).replace(' ','')).objects.all()):
					return view(request, modelo, key)
				else:
					return render_to_response('404.html')
			else:	
				return view(request, modelo)
		else:
			return render_to_response('404.html')
	return wrapper