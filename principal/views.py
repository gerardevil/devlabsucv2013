#views.py

# Imports for Objects and Managers bellow
from django.db.models.loading import get_app, get_models, get_model
from principal.manager.decorators import *
from principal.manager import entity
from principal.models import *
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

#Profesor
@login_required
def profile(request):
    try:
        u = Usuario.objects.get(usuario_id=request.user)
        usr = u.toString()
        centro = u.centro.toString()
        materiasS = MateriaSolicitada.objects.all().filter(usuario=u).order_by("id")
        horariosS = HorarioSolicitado.objects.filter(horario_solicitado__in = materiasS).order_by("horario_solicitado")

        if request.method == 'POST':
            form = AgregarMateriaForm(request.POST)
            cant_hor = int(request.POST['cantidad_hor'])

            if form.is_valid() and cant_hor:

                cse = MateriaSolicitada.objects.filter(estatus='R',usuario=u,materia=form.cleaned_data['materia']).count()
                if (cse == 0):
                    ms = MateriaSolicitada(estatus='R',usuario=u,materia=form.cleaned_data['materia'])
                    ms.save()
                else:
                    ms = MateriaSolicitada.objects.get(usuario=u,materia=form.cleaned_data['materia'])
                for ind in range(1,cant_hor+1):
                    cad = 'horario'+str(ind)
                    h = HorarioMateria.objects.get(pk=request.POST[cad])
                    HorarioSolicitado.objects.create(dia_semana=h.dia_semana,hora_inicio=h.hora_inicio,hora_fin=h.hora_fin,horario_solicitado=ms,aula=form.cleaned_data['aula'])

                form = AgregarMateriaForm()
                materiasS = MateriaSolicitada.objects.all().filter(usuario=u).order_by("id")
                horariosS = HorarioSolicitado.objects.filter(horario_solicitado__in = materiasS).order_by("horario_solicitado")
                return render_to_response('Principal_Prof.html' ,{'usuario':usr,'centro':centro,'form':form,'info':'La materia ha sido agregada de manera exitosa', 'listaHorarios' : horariosS},context_instance=RequestContext(request))
            else:
                return render_to_response('Principal_Prof.html' ,{'usuario':usr,'centro':centro,'form' : form,'error':'El formulario no es valido', 'listaHorarios' : horariosS},context_instance=RequestContext(request))
        else:
            form = AgregarMateriaForm()
        return render_to_response('Principal_Prof.html' ,{'usuario':usr,'centro':centro,'form' : form, 'listaHorarios' : horariosS },context_instance=RequestContext(request))
    except Warning as w:
        return render_to_response('Principal_Prof.html' ,{'usuario':usr,'centro':centro,'form' : form,'error':w.__doc__ , 'listaHorarios' : horariosS} ,context_instance=RequestContext(request))

@login_required
def borrar_propuesta(request,key):
    m.borrar('horario solicitado',key)
    return HttpResponseRedirect('/profile')

@login_required
def editar_propuesta(request,key):
    try:
        u = Usuario.objects.get(usuario_id=request.user)
        usr = u.toString()
        centro = u.centro.toString()
        model = get_model('principal','horariosolicitado')
        o = model.objects.get(pk=key)
        if request.method == 'POST':
            form = m.generarFormulario(request,'horariosolicitado', o, 1)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/profile')
        else:
            form = m.generarFormulario(request,'horariosolicitado', o, 2)
        return render_to_response('EditarPropM_Prof.html' ,{'form':form,'usuario':usr,'centro':centro},context_instance=RequestContext(request))
    except Warning as w:
        return render_to_response('EditarPropM_Prof.html' ,{'error':w.__doc__},context_instance=RequestContext(request))

@login_required
def editar_profesor(request):
    u = Usuario.objects.get(usuario_id=request.user)
    usr = u.toString()
    centro = u.centro.toString()
    return render_to_response('Perfil_Prof.html',{'usuario':usr,'centro':centro},context_instance=RequestContext(request))

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
def horario(request):
    return render_to_response('HorarioPlanificacion.html',{'listaHorarios': [7,8,9,10,11,12,1,2,3,4,5,6]})

def editarPerfil(request):
    form=CustomUserForm(request.POST)
    return render_to_response('editarPerfil_Prof.html', {'form':form},context_instance=RequestContext(request))    
    #return render_to_response('editarPerfil_Prof.html',context_instance=RequestContext(request))    

def guardarPerfil(request):
    #save()
    return HttpResponseRedirect('/profile')

@login_required
@coordinatorRequired
def getScheduleByRequest(request,rol):
    if request :
        rol_pattern = rol.lower()
        if rol_pattern == 'cc':
            '''Obtenemos a que centro pertenece el Coordinador'''
            centro = Usuario.objects.get(usuario_id=request.user.pk).centro

            try:
                '''Seleccionamos las Materias Solicitadas por usuarios del centro actual '''
                center_request_subject_list=MateriaSolicitada.objects.filter(usuario__centro=centro.pk)

                requested_subject =[e['id'] for e in center_request_subject_list.values('id')]

                '''Seleccionamos los horarios solicitados para estas Materias '''
                center_schedule_list = HorarioSolicitado.objects.filter(horario_solicitado__in=requested_subject)

                '''
                Formato Posicional Json de Retorno:
                [0]materia_id, [1]materia_solicitada_id, [2]username ,
                [3]nombre , [4]dia_seman, [5]hora_inicio, [6]hora_fin
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

                return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json")

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


@login_required
@coordinatorRequired
def getUserByCenter(request):
    centro = Usuario.objects.get(usuario_id=request.user.pk).centro
    center_user_list = Usuario.objects.filter(centro_id=centro.pk).values('usuario_id')
    center_user_list = [e['usuario_id'] for e in center_user_list]
    final_user_list = User.objects.filter(pk__in=center_user_list).order_by('first_name','last_name','username').values('username','first_name','last_name')

    counter = 0
    jsontemp = {}
    for u in final_user_list:
        jsontemp.update({
            counter:{
            'username':final_user_list[counter]['username'],
            'name': final_user_list[counter]['first_name']+' '+final_user_list[counter]['last_name']}
            })
        counter +=1;

    jsontemp.update({'length':counter})

    return HttpResponse(json.dumps(jsontemp, sort_keys=True),content_type="application/json")


@login_required
@coordinatorRequired
def getSubjectByRequest(request):
	centro = Usuario.objects.get(usuario_id=request.user.pk).centro
	center_request_subject_list=MateriaSolicitada.objects.filter(usuario__centro=centro.pk).order_by('materia__materia__nombre').values('materia__materia__pk','materia__materia__nombre')
	jsontemp = {}
	counter = 0
	names = []
	for e in center_request_subject_list:
		if e['materia__materia__nombre'] not in names:
			jsontemp.update({counter:{'id':e['materia__materia__pk'],'nombre':e['materia__materia__nombre']}})
			names.append(e['materia__materia__nombre'])
			counter+=1
	
	jsontemp.update({'length':counter})

	return HttpResponse(json.dumps(jsontemp, sort_keys=True),content_type="application/json")		
