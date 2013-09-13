#views.py

# Imports for Objects and Managers bellow
from django.db.models.loading import get_app, get_models, get_model
import sys
from principal.manager.decorators import *
from principal.manager import entity
from principal.models import *

# Imports for validation or any other thing bellow
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType 
from django.http import HttpResponse ,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.core import serializers
from django.http import Http404
from principal.forms import *
import json
import os

#Entity manager class' Unique instance of 
m = entity.Manager()

def inicio(request):
	return render_to_response('Home.html')

# Login view
def loginUser(request):	
	login_form =  LoginForm(request.POST)

	if request.POST and  login_form.is_valid():
		username = request.POST['user']
		password = request.POST['password']
		if User.objects.filter(username=username).exists() :

			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)

				if request.GET and 'next' in request.GET:

					try:
						return HttpResponseRedirect(request.GET['next']) 
					except Exception, e:
						raise Http404
						
				else:
					return HttpResponseRedirect('/profile')
			else:
				return render_to_response('Login.html' ,{'err':2,'login_form' : login_form},context_instance=RequestContext(request))

		else:
			return render_to_response('Login.html' ,{'err':1,'login_form' : login_form},context_instance=RequestContext(request))
	else:	
		return render_to_response('Login.html',{'login_form' : login_form},context_instance=RequestContext(request))

# Logout view
@login_required
def logoutUser(request):
	logout(request)
	return render_to_response('Home.html')

@login_required
def profile(request):
	return render_to_response('Principal_Prof.html')	

	
# CRUD Materia Begin:
def ppalCrudMaterias(request):
	materias = Materia.objects.all().order_by('nombre')
	return render_to_response('PpalMaterias_Admin.html', {'listaMaterias':materias})

def crearMateria(request):
	centros = Centro.objects.all().order_by('nombre')
	return render_to_response('CrearMateria_Admin.html', {'listaCentros':centros})

def modificarMateria(request):
	return render_to_response('ModificarMateria_Admin.html')

def listarMaterias(request):
	materias = Materia.objects.all()
	#json = serializers.serialize('json',materias)
	temp = [m.toJson() for m in materias]
	return HttpResponse(json.dumps(temp), content_type="application/json")
	
def obtenerMateria(request):
	materia = Materia.objects.get(pk=request.GET['id'])
	return HttpResponse(json.dumps(materia.toJson(False)), content_type="application/json")
	
def guardarMateria(request):

	if 'centro' in request.GET:
		centro = Centro.objects.get(pk=request.GET['centro'])
	else:
		centro=None
	materia = Materia(materia_id=request.GET['id'],
					  nombre = request.GET['nombre'],
					  tipo_materia = request.GET['tipo'],
					  unidades_credito_teoria = request.GET['uct'],
					  unidades_credito_practica = request.GET['ucp'],
					  unidades_credito_laboratorio = request.GET['ucl'],
					  estatus = request.GET['estatus'],
					  semestre=request.GET['semestre'],
					  centro=centro)
	materia.save()
	return HttpResponse('<h2>Operaci&oacute;n realizada satisfactoriamente</h2>')
	
def eliminarMateria(request):
	materia = Materia.objects.get(pk=request.GET['id'])
	materia.delete()
	return HttpResponse('<h2>Operaci&oacute;n realizada satisfactoriamente</h2>')

# CRUD Materia End.

# Admin principal views :

@login_required
def admins(request):
	return render_to_response('Principal_Admin.html',{'opc':1})

@login_required
def listarm(request):
	'''Metodo que lista todos los modelos'''
	clases_modelos = []
	apps = get_app('principal')
	for model in get_models(apps):
		mn = model._meta.verbose_name
		clases_modelos.append({'nombre': mn,'nombre_se': mn.replace(' ','')})
	return render_to_response('Principal_Admin.html',{'modelos':clases_modelos,'opc':2})

# CRUD Generico Begin

@login_required
@validateInputCrudData
def insertar(request,modelo):
	try:
		'''Metodo generico para insertar'''
		form = m.generarFormulario(request,modelo,None,0)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/admins/modelos/'+modelo)
		return render_to_response('Insertar.html' ,{'form' : form,'opc':5,'modelo':modelo},context_instance=RequestContext(request))
	except Warning as w:
		return render_to_response('Insertar.html' ,{'form' : form,'opc':5,'modelo':modelo,'error':w.__doc__} ,context_instance=RequestContext(request))

@login_required
@validateInputCrudData
def listar(request,modelo):
	'''Metodo que lista todos los objetos de un modelo'''
	return render_to_response('Principal_Admin.html',{'lista': m.listar(str(modelo)), 'opc': 3, 'modelo' : modelo})

@login_required
@validateInputCrudData
def borrar(request, modelo, key):
	'''Metodo generico para borrar'''
	m.borrar(modelo,key)
	return HttpResponseRedirect('/admins/modelos/'+modelo)

@login_required
@validateInputCrudData
def editar(request,modelo,key):
	try:
		'''Metodo generico para editar'''
		model = get_model('principal',str(modelo).replace(' ',''))
		o = model.objects.get(pk=key)
		if request.method == 'POST':
			form = m.generarFormulario(request, modelo, o, 1)
			if form.is_valid():
				if modelo=='usuario':
					form.save(o.usuario_id.username)
				else:
					form.save()
				return HttpResponseRedirect('/admins/modelos/'+modelo)
		else:
			form = m.generarFormulario(request, modelo, o, 2)
		return render_to_response('Insertar.html' ,{'form' : form,'opc':5,'modelo':modelo},context_instance=RequestContext(request))
	except Warning as w:
		return render_to_response('Insertar.html' ,{'form' : form,'opc':5,'modelo':modelo,'error':w.__doc__},context_instance=RequestContext(request))
	
@login_required
@validateInputCrudData	
def leer(request,modelo,key):
	'''Metodo generico para leer'''
	objeto = m.leer(modelo,key)
	return render_to_response('Principal_Admin.html' ,{'objeto':objeto,'modelo':modelo,'opc':4,'modelo':modelo},context_instance=RequestContext(request))

#END CRUD Generico


def horario(request):
	return render_to_response('HorarioPlanificacion.html',{'listaHorarios': [7,8,9,10,11,12,1,2,3,4,5,6]})

# Coordinador Features #
########################

'''Only for development usage '''
def getTemplate(request,template):
	return render_to_response(template)


