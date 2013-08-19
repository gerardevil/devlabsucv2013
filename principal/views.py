# Imports for Objects and Managers bellow
from django.db.models.loading import get_app, get_models, get_model
from principal.models import Usuario, Rol, UsuarioRol, Materia, Centro
from principal.manager import entity
# Imports for validation or any other thing bellow
from django.http import HttpResponse ,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core import serializers
from principal.forms import *
import os
import json

from django.contrib.contenttypes.models import ContentType 


m = entity.Manager()

def inicio(request):
    return render_to_response('Home.html')

# Login V3 session control
def login(request):
	
	login_form =  LoginForm(request.POST)
	if request.POST and  login_form.is_valid():
		user_ext = request.POST['user']
		password_ext = request.POST['password']
		
		try:
			password = Usuario.objects.get(usuario_id=int(user_ext)).clave
		except Exception, e:
			return render_to_response('Login.html' ,{'err':1,'login_form' : login_form},context_instance=RequestContext(request))
		else:
				if password_ext == password:
				
					SesionActiva().save(int(user_ext))	
					return HttpResponseRedirect('/profile')

				else:
					return render_to_response('Login.html' ,{'err':2,'login_form' : login_form},context_instance=RequestContext(request))							
	else:
		return render_to_response('Login.html',{'login_form' : login_form},context_instance=RequestContext(request))

#@is_loged
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

################################################################
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

def admins(request):
    #return render(request,'Principal_Admin.html')
    return render_to_response('Principal_Admin.html',{'opc':1})

def listarm(request):
	'''Metodo que lista todos los modelos'''
	clases_modelos = []
	apps = get_app('principal')
	for model in get_models(apps):
		mn = model._meta.verbose_name
		clases_modelos.append({'nombre': mn,'nombre_se': mn.replace(' ','')})
	return render_to_response('Principal_Admin.html',{'modelos':clases_modelos,'opc':2})

# CRUD Generico
def insertar(request,modelo):
	'''Metodo generico para insertar'''
	form = m.generarFormulario(request,modelo,None,0)
	if form.is_valid():
		form.save()
		return render_to_response('listarUsuarios.html')
	return render_to_response('Insertar.html' ,{'form' : form},context_instance=RequestContext(request))

def listar(request,modelo):
	'''Metodo que lista todos los objetos de un modelo'''
	return render_to_response('Principal_Admin.html',{'lista': m.listar(str(modelo)), 'opc': 3, 'modelo' : modelo})

def borrar(request, modelo, key):
	'''Metodo generico para borrar'''
	m.borrar(modelo,key)
	return render_to_response('Principal_Admin.html',{'lista': m.listar(str(modelo)), 'opc': 3, 'modelo' : modelo})

def editar(request,modelo,key):
	'''Metodo generico para editar'''
	model = get_model('principal',modelo)
	o = model.objects.get(pk=key)
	form = None
	if request.method == 'POST':
		form = m.generarFormulario(request, modelo, o, 1)
		if form.is_valid():
			form.save()
			return render_to_response('Principal_Admin.html',{'lista': m.listar(str(modelo)), 'opc': 3, 'modelo' : modelo})
	else:
		form = m.generarFormulario(request, modelo, o, 2)
	return render_to_response('Insertar.html' ,{'form' : form},context_instance=RequestContext(request))

