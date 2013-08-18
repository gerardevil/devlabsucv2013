from django.db.models.loading import get_app, get_models, get_model
from principal.models import *
from django.contrib.contenttypes.models import ContentType 
from principal.forms import *
from django.shortcuts import render_to_response
from django.template.context import RequestContext

class Manager:

	def __init__(self):
		pass

	def listar(self, modelName):
		claseModelo = get_model('principal',str(modelName).replace(' ',''))
		return claseModelo.objects.all()

	def generarFormulario(self,request,modelo,inst,case):
		model = get_model('principal',modelo)
		type_id = ContentType.objects.get_for_model(model).id
		form_class = get_object_form(type_id)
		if case == 0:
			form = form_class(request.POST, None)
		if case == 1:
			form = form_class(request.POST, instance=inst)
		if case == 2:
			form = form_class(instance=inst)
		return form

	def borrar(self, modelo, key):
		model = get_model('principal',modelo)
		o = model.objects.get(pk=key)
		#Verificar si el objeto existe
		o.delete()
		return None

