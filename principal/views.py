# Imports for Objects bellow
from django.db.models.loading import get_app, get_models, get_model
from principal.models import Usuario, Rol, UsuarioRol, Materia, Centro
# Imports for validation or any other thing bellow
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core import serializers
import os



def inicio(request):
    return render_to_response('Home.html')

# Login v0 by using GET, must be by using CSRF by POST
def login(request):
	user_ext = request.GET['user']
	password_ext = request.GET['password']
	
	if user_ext and password_ext:
		try:
			password = Usuario.objects.get(usuario_id=int(user_ext)).clave
		except Exception, e:
            #return HttpResponse('<h2>User not found</h2>')
			return render_to_response("Home.html",{'err':2})
		else:
				if password_ext == password:
					return render_to_response('Principal_Prof.html')
                    #return render_to_response(<frontend_error_view>)
				else:
                    #return HttpResponse('<h2>Invalid password</h2>')
					return render_to_response("Home.html",{'err':3})
	else:
		return render_to_response("Home.html",{'err':1})
		
# CRUD Materia Begin:

def listarMaterias(request):
	materias = Materia.objects.all()
	json = serializers.serialize('json',materias)
	return HttpResponse(json, content_type="application/json")
	
def obtenerMateria(request):
	materia = Materia.objects.get(pk=request.GET['id'])
	json = serializers.serialize('json',[materia])
	return HttpResponse(json, content_type="application/json")
	
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
    clases_modelos = []
    apps = get_app('principal')
    for model in get_models(apps):
        mn = model._meta.verbose_name

        clases_modelos.append({'nombre': mn,'nombre_se': mn.replace(' ','')})

    return render_to_response('Principal_Admin.html',{'modelos':clases_modelos,'opc':2})

def datos(request,modelo):
    clase_modelo = get_model('principal',str(modelo).replace(' ',''))
    lista = clase_modelo.objects.all()
    return render_to_response('Principal_Admin.html',{'modelo':modelo,'opc':3,'lista':lista})
#    return HttpResponse(modelo)

#Views for Usuario
def insertarUsuario(request):
	user_form = UsuarioForm(request.POST)
	if user_form.is_valid():
		user_form.save()
		return render_to_response('listarUsuarios.html')
	return render_to_response('insertarUsuario.html' ,{'user_form' : user_form},context_instance=RequestContext(request))

def listarUsuarios(request):
	usuarios = Usuario.objects.all()
	return render_to_response('listarUsuarios.html', {'usuarios' : usuarios})

def borrarUsuario(request, usuario_id):
	p = Usuario.objects.get(pk=usuario_id)
	p.delete()
	return render_to_response('listarUsuarios.html')

def editarUsuario(request,usuario_id):
	p = Usuario.objects.get(pk=usuario_id)
	user_form = UsuarioForm(request.POST, instance=p)
	if user_form.is_valid():
		user_form.save()
		return render_to_response('listarUsuarios.html')
	return render_to_response('insertarUsuario.html' ,{'user_form' : user_form},context_instance=RequestContext(request))