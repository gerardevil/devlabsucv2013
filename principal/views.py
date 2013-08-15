# Imports for Objects bellow
from principal.models import Usuario, Rol, UsuarioRol
# Imports for validation or any other thing bellow
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
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

