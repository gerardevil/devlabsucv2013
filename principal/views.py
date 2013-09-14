#views.py

# Imports for Objects and Managers bellow
from django.db.models.loading import get_app, get_models, get_model
from principal.manager.decorators import *
from principal.manager import entity
from principal.models import *
from django.contrib.auth.models import User
import sys

# Imports for validation or any other thing bellow
from principal.manager.converters import convertDatetimeToString
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
		login_form =  LoginForm()
		return render_to_response('Login.html',{'login_form' : login_form},context_instance=RequestContext(request))

# Logout view
@login_required
def logoutUser(request):
	logout(request)
	return render_to_response('Home.html')


@login_required
def profile(request):
    try:
        if request.method == 'POST':
            form = AgregarMateriaForm(request.POST)
            if form.is_valid():

                u = Usuario.objects.get(usuario_id=request.user)
                ms = MateriaSolicitada(estatus='R',usuario=u,materia=form.cleaned_data['materia'])
                h = HorarioMateria.objects.get(pk=request.POST['horario1'])
                #hs = HorarioSolicitado(dia_semana=h.dia_semana,hora_inicio=h.hora_inicio,hora_fin=h.hora_fin,horario_solicitado=ms,aula=form.cleaned_data['aula'])
                ms.save()
                HorarioSolicitado.objects.create(dia_semana=h.dia_semana,hora_inicio=h.hora_inicio,hora_fin=h.hora_fin,horario_solicitado=ms,aula=form.cleaned_data['aula'])
                form = AgregarMateriaForm()
                #return render_to_response('Principal_Prof.html' ,{'form':form,'info':str(h)},context_instance=RequestContext(request))
                return render_to_response('Principal_Prof.html' ,{'form':form,'info':'La materia ha sido agregada de manera exitosa'},context_instance=RequestContext(request))
            else:
                return render_to_response('Principal_Prof.html' ,{'form' : form,'error':'El formulario no es valido :('},context_instance=RequestContext(request))
        else:
            form = AgregarMateriaForm()
        return render_to_response('Principal_Prof.html' ,{'form' : form},context_instance=RequestContext(request))
    except Warning as w:
        return render_to_response('Principal_Prof.html' ,{'form' : form,'error':w.__doc__} ,context_instance=RequestContext(request))


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

#Profesor
@login_required
def horarios_materia(request):
    if request.is_ajax():
        key = request.POST['mat_sel']
        mat = MateriaOfertada.objects.get(pk=int(key)).materia
        lista_horarios = HorarioMateria.objects.filter(materia=mat)
        lista_horarios_json = [h.toJson() for h in lista_horarios]
        return HttpResponse(json.dumps(lista_horarios_json), mimetype='application/javascript')
    else:
        return HttpResponse('Fallo en AJAX')


@login_required
def horario(request):
	return render_to_response('HorarioPlanificacion.html',{'listaHorarios': [7,8,9,10,11,12,1,2,3,4,5,6]})

@login_required
def getHorariosSolicitados(request,rol):
	if request :
		rol_pattern = rol.lower()
		if rol_pattern == 'cc':
			'''Obtenemos a que centro pertenece el Coordinador'''			
			centro = Usuario.objects.get(usuario_id=request.user.pk).centro
			
			try:
				'''Seleccionamos los usuarios que pertenecen al centro actual'''
				center_user_list = Usuario.objects.filter(centro_id=centro.pk)
				users = [e['id'] for e in center_user_list.values('id')]

				'''Seleccionamos las Materias Solicitadas por estos usuario '''		
				center_request_subject_list=MateriaSolicitada.objects.filter(usuario__in=users)
				
				requested_subject =[e['id'] for e in center_request_subject_list.values('id')]

				'''Seleccionamos los horarios solicitados para estas Materias '''
				center_schedule_list = HorarioSolicitado.objects.filter(horario_solicitado__in=requested_subject) 

				'''
				Formato Posicional Json de Retorno:

				[0]materia_id, 
				[1]materia_solicitada_id, 
				[2]username , 
				[3]nombre , 
				[4]dia_seman, 
				[5]hora_inicio, 
				[6]hora_fin				
				'''
				jsontmp = {}
				counter = 0
				for h in center_schedule_list:
					jsontmp.update(
					{
					counter:	{
					 'materia_id': h.horario_solicitado.materia.materia.pk,
					 'materia_solicitada':h.pk,
					 'horario_solicitado':h.horario_solicitado.pk,
					 'username':h.horario_solicitado.usuario.usuario_id.username,
					 'nombre':h.horario_solicitado.materia.materia.nombre,
					 'dia_semana':h.dia_semana,
					 'hora_inicio':convertDatetimeToString(h.hora_inicio),
					 'hora_fin':convertDatetimeToString(h.hora_fin)}
					}
					)
					counter +=1		
							
				jsontmp.update({'length':counter})
				
					
				return  HttpResponse(json.dumps(jsontmp), content_type="application/json")		

			except Exception, e:
				raise e

		elif  rol_pattern == 'jdd':
			'''El usuario es un Jefe de Departamento obtiene todos los horarios 
			de la Escuela de Computacion'''
			pass
		else:
			raise Http404
	else:
		raise Http404;

	return HttpResponse('Hello	World')

def getUsuarioCentro(request,rol):
	pass

def getMateriasSolicitadasCentro(request,rol):
	pass
