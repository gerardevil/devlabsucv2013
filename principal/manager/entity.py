#entity.py

from principal.forms import *
from principal.models import *
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models.loading import get_app, get_models, get_model
from django.contrib.contenttypes.models import ContentType 
from django.core.mail import send_mass_mail
import smtplib

class Manager:

	def __init__(self):
		pass

	def listar(self, modelName):
		claseModelo = get_model('principal',str(modelName).replace(' ',''))
		return claseModelo.objects.all()

	def generarFormulario(self,request,modelo,inst,case):
		model = get_model('principal',str(modelo).replace(' ',''))
		type_id = ContentType.objects.get_for_model(model).id
		if modelo == 'usuario':
			if case == 0: 
				return CustomUserForm(True,request.POST)
			elif case == 1:
				return CustomUserForm(False,request.POST,inst.toJson(False))
			elif case == 2:
				return CustomUserForm(False, inst.toJson(False))
		else:
			form_class = get_object_form(type_id)
			if case == 0:
				return form_class(request.POST)
			elif case == 1:
				return form_class(request.POST, instance=inst)
			elif case == 2:
				return form_class(instance=inst)

	def borrar(self, modelo, key):
		model = get_model('principal',str(modelo).replace(' ',''))
		o = model.objects.get(pk=key)
		if modelo == 'usuario':
			user = User.objects.get(pk = o.usuario_id.pk)
			user.delete()
		o.delete()
		return None
		
	def leer(self, modelo, key):
		model = get_model('principal',str(modelo).replace(' ',''))
		o = model.objects.get(pk=key)
		#Verificar si el objeto existe
		return o
		
	def enviarMail(self,contenido=[]):
		if len(contenido):
			r = tuple()
			for i in xrange(len(contenido)):
				r = r.__add__((contenido[i],))
			print r
			try:
				send_mass_mail(r,fail_silently=True)
			except smtplib.SMTPException, s:raise s
			return True
		else: 
			return False	
	