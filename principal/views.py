
#encoding:utf-8

#views.py

# Imports for Objects and Managers bellow
from django.db.models.loading import get_app, get_models, get_model
from principal.manager.converters import translateStatus
from django.contrib.auth.models import User
from principal.manager.decorators import *
from principal.manager import entity
from principal.models import *
import sys
import csv

# Imports for validation or any other thing bellow
from principal.manager.converters import convertDatetimeToString
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType 
from django.http import HttpResponse ,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.core import serializers
from django.conf import settings
from django.core import signing
from django.http import Http404
from principal.forms import *
import os,re,json,datetime


#Entity manager class' Unique instance of 
m = entity.Manager()

###########
# General #
###########

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
        login_form =  LoginForm(request.POST)
        return render_to_response('Login.html',{'login_form' : login_form},context_instance=RequestContext(request))

# Logout view
@login_required
def logoutUser(request):
    logout(request)
    return render_to_response('Home.html')

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

@login_required
@validateInputCrudDataEdit
def cambiarContrasena(request,rol, key):
    try:
        o = Usuario.objects.get(pk=key)
        roles = UsuarioRol.objects.filter(cedula=o)
        usr = User.objects.get(username=request.user.username)
        form=CambiarContrasena(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                contrasenaVieja = request.POST['contrasenaVieja']
                contrasenaNueva = request.POST['contrasenaNueva']
                confirmarContrasena = request.POST['confirmarContrasena']
                
                if (check_password(contrasenaVieja, usr.password)) and (contrasenaNueva == confirmarContrasena):               
                    usr.set_password(confirmarContrasena)
                    usr.save()
                    if rol =='jdd':
                        return HttpResponseRedirect('/profilejdd')
                    elif rol=='cc':
                        return HttpResponseRedirect('/profilecc')
                    elif rol == 'p':
                        return HttpResponseRedirect('/profile')
                    else:
                        raise Http404 
                else:
                    return HttpResponse("Datos de contraseña invalidos")
            return render_to_response('cambiarContrasena.html', {'usuario':request.user.first_name+" "+request.user.last_name,'centro':o.centro.nombre,'form' : form,'rol':rol,'pk':key, 'roles':roles},context_instance=RequestContext(request))
        else:
            return render_to_response('cambiarContrasena.html', {'usuario':request.user.first_name+" "+request.user.last_name,'centro':o.centro.nombre,'form' : form,'rol':rol,'pk':key, 'roles':roles},context_instance=RequestContext(request))
    except Warning as w:
        return render_to_response('cambiarContrasena.html', {'usuario':request.user.first_name+" "+request.user.last_name,'centro':o.centro.nombre,'form' : form,'rol':rol,'pk':key, 'roles':roles, 'error':w.__doc__},context_instance=RequestContext(request))

@login_required
@validateInputCrudDataEdit
def editarperfil(request,rol,key):
    try:
        o = Usuario.objects.get(pk=key)
        roles = UsuarioRol.objects.filter(cedula=o)
        if request.method == 'POST':
            form = m.generarFormulario(request, 'usuario', o, 1)
            if form.is_valid():
                form.save(o.usuario_id.username)
                if rol =='jdd':
                    return HttpResponseRedirect('/profilejdd')
                elif rol=='cc':
                    return HttpResponseRedirect('/profilecc')
                elif rol == 'p':
                    return HttpResponseRedirect('/profile')
                else:
                    raise Http404
        else:
            form = m.generarFormulario(request, 'usuario', o, 2)
        return render_to_response(str(rol)+'Editar.html' ,{'usuario':request.user.first_name+" "+request.user.last_name,'centro':o.centro.nombre,'form' : form, 'rol':rol,'pk':key, 'roles':roles},context_instance=RequestContext(request))
    except Warning as w:
        return render_to_response(str(rol)+'Editar.html' ,{'usuario':request.user.first_name+" "+request.user.last_name,'centro':o.centro.nombre,'form' : form,'rol':rol,'pk':key, 'roles':roles, 'error':w.__doc__},context_instance=RequestContext(request))


def resetPasswordRequest(request):
    if request:
        try:
            form = ResetPasswordRequestForm(request.POST)
            notes = "Ingrese su numero de documento de indentidad, posteriormente enviaremos instrucciones a la cuenta de correo electronico asociada para restaurar su contraseña."
            if form.is_valid():       
                return resetPasswordSendEmail(request)
            else:
                return render_to_response('resetPasswordRequest.html' ,{'form' : form, 'notes':notes} ,context_instance=RequestContext(request))
        except Warning as w:
            return render_to_response('resetPasswordRequest.html' ,{'form' : form, 'notes':notes,'error':w.__doc__} ,context_instance=RequestContext(request))
    else:
        return Http404

def resetPasswordSendEmail(request):
    if request and request.POST:
        usr = request.POST['username']        
        profile = User.objects.get(username=usr)
        currentURL = request.build_absolute_uri()
        resetURL = currentURL[:[r.start() for r in re.finditer('/',currentURL)][2]]+'/reset/?token='
        token = signing.dumps(usr,salt=settings.HEAVEN_KEY)
        resetURL +=  token

        content = u"Hola, "+profile.first_name+u" "+profile.last_name+u".\n"
        content += u"Hemos recibido una solicitud de cambio de contraseña a tu nombre, "
        content += u"emplea el siguiente link para acceder al proceso de restauración de contraseña:\n\n"
        content += resetURL
        m.enviarMail([m.makeMessage(to=[profile.email],content=content)])       

        OneTimeUseURL.objects.create(url=token)
        return HttpResponseRedirect('/')
    else:
        return Http404

def resetPasswordChangeIt(request):
    if request and request.method=='GET' and 'token' in request.GET:
        if OneTimeUseURL.objects.filter(url=request.GET['token']).exists():
            try:

                usr = signing.loads(request.GET['token'],salt=settings.HEAVEN_KEY,max_age=settings.RESET_PASSWORD_TIMEOUT)
                form = ResetPasswordChangeForm(request.POST)
                return render_to_response('resetPasswordChange.html' ,{'form' : form} ,context_instance=RequestContext(request))

            except signing.BadSignature, b:

                notes = u"El siguiente url :  <font color='blue'><b>"+request.build_absolute_uri()+"</b></font>,  posee problemas en su firma digital intente realizar el proceso de recuperaci&oacuten de contrase&ntildea una vez m&aacutes."
                return render_to_response('resetPasswordErrors.html',{'notes':notes})

            except signing.SignatureExpired, s:

                notes = u"El siguiente url :  <font color='blue'><b>"+request.build_absolute_uri()+"</b></font>,  ya ha expirado, intente realizar el proceso de restauraci&oacuten una vez m&aacutes."
                return render_to_response('resetPasswordErrors.html',{'notes':notes})

        else:

            notes = u"El siguiente url :  <font color='blue'><b>"+request.build_absolute_uri()+"</b></font>,  ya ha sido empleado para realizar el proceso de restauraci&oacuten de contrase&ntildea &oacute es incorrecto, intente realizar el proceso una vez m&aacutes."
            return render_to_response('resetPasswordErrors.html',{'notes':notes})

    elif request and request.method == 'POST' and 'token' in request.GET:
        try:
            form = ResetPasswordChangeForm(request.POST)
            if form.is_valid():
                
                if form.cleaned_data['password']==form.cleaned_data['password_confirm']:
                    try:
                        cedula = signing.loads(request.GET['token'],salt=settings.HEAVEN_KEY,max_age=settings.RESET_PASSWORD_TIMEOUT)
                        usr = User.objects.get(username=cedula)
                        usr.set_password(form.cleaned_data['password'])
                        usr.save()
                        OneTimeUseURL.objects.filter(url=request.GET['token']).delete()
                        return HttpResponseRedirect('/login')
                    except signing.BadSignature, b:

                        notes = u"El siguiente url :  <font color='blue'><b>"+request.build_absolute_uri()+"</b></font>,  posee problemas en su firma digital intente realizar el proceso de recuperaci&oacuten de contrase&ntildea una vez m&aacutes."
                        return render_to_response('resetPasswordErrors.html',{'notes':notes})

                    except signing.SignatureExpired, s:

                        notes = u"El siguiente url :  <font color='blue'><b>"+request.build_absolute_uri()+"</b></font>,  ya ha expirado, intente realizar el proceso de restauraci&oacuten una vez m&aacutes."
                        return render_to_response('resetPasswordErrors.html',{'notes':notes})
                else:
                    return render_to_response('resetPasswordChange.html' ,{'form' : form,'err':1} ,context_instance=RequestContext(request))
                return render_to_response('resetPasswordChange.html' ,{'form' : form} ,context_instance=RequestContext(request))
        except Warning as w:
            return render_to_response('resetPasswordRequest.html' ,{'form' : form,'error':w.__doc__} ,context_instance=RequestContext(request))
    else:
        return Http404 

@login_required
@csrf_protect
def Contact(request):
    if request.is_ajax() and request and request.method=='POST' and 'to' in request.POST and 'message' in request.POST and 'matter' in request.POST :
        try:
            to = request.POST['to']
            if ';' in to:
                to = request.POST['to'].split(';')
                to.remove('')
            content=  request.POST['message']
            subject = request.POST['matter']

            if (content and subject):
                m.enviarMail([m.makeMessage(subject=subject,to=to,content=content)])
            elif(subject):
                m.enviarMail([m.makeMessage(subject=subject,to=to)])
            elif(content):
                m.enviarMail([m.makeMessage(to=to,content=content)])
            else:
                m.enviarMail([m.makeMessage(to=to)])                
            return HttpResponse(status=200)
        except Exception, e:
            raise e
    else:
        raise Http404

############
# Profesor #
############

@login_required
def profile(request):
    try:
        u = Usuario.objects.get(usuario_id=request.user)
        roles = UsuarioRol.objects.filter(cedula=u)
        usr = u.toString()
        centro = u.centro.toString()
        materiasS = MateriaSolicitada.objects.all().filter(usuario=u).order_by("id")
        horariosS = HorarioSolicitado.objects.filter(horario_solicitado__in = materiasS).order_by("horario_solicitado")

        if request.method == 'POST':
            if ('cantidad_hor' in request.POST):
                form = AgregarMateriaForm(request.POST)
                cant_hor = int(request.POST['cantidad_hor'])
                form_e = AgregarMateriaEForm()

                if form.is_valid() and cant_hor:
                    cse = MateriaSolicitada.objects.filter(estatus='N',usuario=u,materia=form.cleaned_data['materia']).count()
                    if (cse == 0):
                        ms = MateriaSolicitada(estatus='N',usuario=u,materia=form.cleaned_data['materia'])
                        ms.save()
                    else:
                        ms = MateriaSolicitada.objects.get(usuario=u,materia=form.cleaned_data['materia'])
                    for ind in range(1,cant_hor+1):
                        cad = 'horario'+str(ind)
                        h = HorarioMateria.objects.get(pk=request.POST[cad])
                        HorarioSolicitado.objects.create(dia_semana=h.dia_semana,hora_inicio=h.hora_inicio,hora_fin=h.hora_fin,horario_solicitado=ms)

                    form = AgregarMateriaForm()
                    materiasS = MateriaSolicitada.objects.all().filter(usuario=u).order_by("id")
                    horariosS = HorarioSolicitado.objects.filter(horario_solicitado__in = materiasS).order_by("horario_solicitado")
                    return render_to_response('Principal_Prof.html' ,{'usuario':usr,'roles':roles, 'pk':u.pk, 'centro':centro,'form':form,'form_e':form_e,'info':'La materia ha sido agregada de manera exitosa', 'listaHorarios' : horariosS},context_instance=RequestContext(request))
                else:
                    return render_to_response('Principal_Prof.html' ,{'usuario':usr,'roles':roles, 'pk':u.pk, 'centro':centro,'form' : form,'form_e':form_e,'error':'El formulario no es valido', 'listaHorarios' : horariosS},context_instance=RequestContext(request))
            else:
                form = AgregarMateriaForm()
                form_e = AgregarMateriaEForm(request.POST,ukey=u.pk)
                if form_e.is_valid():
                    form_e.save()
                    form_e = AgregarMateriaEForm(ukey=u.pk)
                    return render_to_response('Principal_Prof.html' ,{'usuario':usr,'roles':roles, 'pk':u.pk, 'centro':centro,'form':form,'form_e':form_e,'info':'La materia ha sido agregada de manera exitosa', 'listaHorarios' : horariosS},context_instance=RequestContext(request))
                else:
                    form_e = AgregarMateriaEForm(ukey=u.pk)
                    return render_to_response('Principal_Prof.html' ,{'usuario':usr,'roles':roles, 'pk':u.pk, 'centro':centro,'form':form,'form_e':form_e,'error':'El formulario no es valido', 'listaHorarios' : horariosS},context_instance=RequestContext(request))
        else:
            form = AgregarMateriaForm()
            form_e = AgregarMateriaEForm(ukey=u.pk)
        return render_to_response('Principal_Prof.html' ,{'usuario':usr,'roles':roles,'pk':u.pk, 'centro':centro,'form' : form,'form_e':form_e, 'listaHorarios' : horariosS },context_instance=RequestContext(request))
    except Warning as w:
        return render_to_response('Principal_Prof.html' ,{'usuario':usr,'roles':roles, 'pk':u.pk, 'centro':centro,'form': form,'form_e':form_e,'error':w.__doc__ , 'listaHorarios' : horariosS} ,context_instance=RequestContext(request))

@login_required
def borrar_propuesta(request,key):
    hs = HorarioSolicitado.objects.get(pk=key)
    if hs.horario_solicitado.estatus == 'N' or hs.horario_solicitado.estatus == 'R':
        ms = hs.horario_solicitado
        hsc = HorarioSolicitado.objects.filter(horario_solicitado=ms).count()
        m.borrar('horario solicitado',key)
        if hsc < 2:
            m.borrar('materia solicitada',ms.pk)
        return HttpResponseRedirect('/profile')
    else:
        return HttpResponseRedirect('/profile')

@login_required
def editar_propuesta(request,key):
    try:
        u = Usuario.objects.get(usuario_id=request.user)
        usr = u.toString()
        centro = u.centro.toString()
        hs = HorarioSolicitado.objects.get(pk=key)
        if hs.horario_solicitado.estatus == 'N' or hs.horario_solicitado.estatus == 'R':
            materia = hs.horario_solicitado.materia.materia
            tipo_mat = materia.tipo_materia
            nm = materia.nombre
            #horarios_mat = HorarioMateria.objects.filter(materia=materia)
            if request.method == 'POST':
                if tipo_mat == 'Electiva' or tipo_mat == 'Complementaria':
                    form = EditarMateriaE(request.POST,hkey=key)
                else:
                    form = EditarMateriaO(request.POST,hkey=key,ukey=u.pk,mat=materia)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/profile')
                else:
                    if tipo_mat == 'Electiva' or tipo_mat == 'Complementaria':
                        form = EditarMateriaE(request.POST,hkey=key)
                    else:
                        form = EditarMateriaO(request.POST,hkey=key,ukey=u.pk,mat=materia)
                    return render_to_response('EditarPropM_Prof.html' ,{'form':form,'error':'Formulario no valido','nombre_mat':nm},context_instance=RequestContext(request))
            else:
                if tipo_mat == 'Electiva' or tipo_mat == 'Complementaria':
                    form = EditarMateriaE(hkey=key)
                else:
                    form = EditarMateriaO(hkey=key,ukey=u.pk,mat=materia)
            return render_to_response('EditarPropM_Prof.html' ,{'form':form,'usuario':usr,'centro':centro,'nombre_mat':nm},context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/profile')
    except Warning as w:
        return render_to_response('EditarPropM_Prof.html' ,{'error':w.__doc__,'nombre_mat':nm},context_instance=RequestContext(request))

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

#########
# Admin #
#########

@login_required
def admins(request):
    usr = Usuario.objects.get(usuario_id = request.user.pk)
    roles = UsuarioRol.objects.filter(cedula=usr)
    return render_to_response('Principal_Admin.html',{'opc':1, 'roles':roles})

@login_required
def listarm(request):
    '''Metodo que lista todos los modelos'''
    usr = Usuario.objects.get(usuario_id = request.user.pk)
    roles = UsuarioRol.objects.filter(cedula=usr)
    clases_modelos = []
    apps = get_app('principal')
    for model in get_models(apps):
        mn = model._meta.verbose_name
        clases_modelos.append({'nombre': mn,'nombre_se': mn.replace(' ','')})
    return render_to_response('Principal_Admin.html',{'modelos':clases_modelos,'opc':2,'roles':roles})

######################################
# Coordinador y Jefe de Departamento #
######################################

@login_required
@coordinatorRequired
def profilecc(request):
    try:
        if request :
            usr = Usuario.objects.get(usuario_id = request.user.pk)
            roles = UsuarioRol.objects.filter(cedula=usr)
            usrcenter = Usuario.objects.filter(centro=usr.centro).order_by('usuario_id__first_name','usuario_id__last_name').values('id','usuario_id__first_name','usuario_id__last_name') 
            return render_to_response("CC_principal.html",{'usuario':request.user.first_name+" "+request.user.last_name,'centro':usr.centro.nombre,'pk':usr.pk, 'roles':roles, 'usrlist':usrcenter},context_instance=RequestContext(request))
        else:
            raise Http404
    except Exception, e:
        raise e

@login_required
@bossRequired
def profilejdd(request):
    try:
        if request :
            usr = Usuario.objects.get(usuario_id = request.user.pk)
            roles = UsuarioRol.objects.filter(cedula=usr)
            usrcenter = Usuario.objects.all().order_by('centro__nombre','usuario_id__first_name','usuario_id__last_name').values('id','centro__nombre','usuario_id__first_name','usuario_id__last_name') 

            newCenter = ''
            headingCount = 1
            genericAccordionDiv = '<div class="acordion" style="margin-left:10%;margin-right:20%;"><div class="acordionCentros" style="min-width:400px;"><div class="accordion" id="accordion2">'
            accordionGroup= '<div class="accordion-group">'
            accordionHeading = '<div class="accordion-heading" >'
            todosCheckBox = '<div class="pull-right custom-align"><input type="checkbox" <name> onClick="toggle(this)" value="none"> Todos</div>'
            nameCenter = '<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" data-toggle="false" <href> > <centerName> </a>'
            accordionBody = '<div <id> class="accordion-body collapse"><div class="accordion-inner">'
            tableHead= '<table><tbody><thead><tr><td><h5>Profesores</h5></td></tr></thead>'
            trContent = '<tr><td><label type="checkbox"><input type="checkbox" <name> <value> onclick = "untoggleAllCheck(this)"><a data-toggle="modal" onclick="getSelectedProfile(<uid>)"> <teacherName> </a></input></label></td></tr>'
            buttonContact = '<button onclick="isAnyCheckSelected()" class="btn btn-primary" type="button" style="float:left;"><i class="icon-envelope icon-white"></i> Contactar Seleccionados</button>'
            endTable = '</table>'
            endTbody = '</tbody>'
            endDiv = '</div>'

            html = genericAccordionDiv
            for u in usrcenter:
                if newCenter != u['centro__nombre']:
                    if html != genericAccordionDiv:
                        html+= endTbody+endTable+ 3*endDiv
                    newCenter = u['centro__nombre']
                    html+= accordionGroup+accordionHeading
                    html+= todosCheckBox.replace('<name>',('name="'+newCenter+'Check"'))
                    html += nameCenter.replace('<href>','href="#'+str(headingCount)+'"').replace('<centerName>',newCenter)
                    html+= endDiv
                    html += accordionBody.replace('<id>' , 'id='+str(headingCount))
                    html+= tableHead
                    headingCount+=1
                html+= trContent.replace('<name>',('name="'+newCenter+'Check"')).replace('<value>','value="'+str(u['id'])+'"').replace('<teacherName>',u['usuario_id__first_name']+' '+u['usuario_id__last_name']).replace('<uid>',str(u['id']))
            html+= endTbody+endTable+ 5*endDiv+buttonContact+endDiv
            return render_to_response("JD_principal.html",{'usuario':request.user.first_name+" "+request.user.last_name,'centro':usr.centro.nombre,'pk':usr.pk, 'roles':roles, 'html':html},context_instance=RequestContext(request))
        else:
            raise Http404
    except Exception, e:
        raise e

@login_required
@coordinatorOrbossRequired
def getEmailList(request):
    try:
        if request.is_ajax() and request and request.method=='GET':
            keys = map((lambda x : int(x)),request.GET['keys'].split(","))
            final = Usuario.objects.filter(id__in=keys).values('usuario_id__email')
            emails = ''
            for f in final:
                if(f['usuario_id__email']!=''):
                    emails+=f['usuario_id__email']+';'
            return HttpResponse(emails)
        else:
            raise Http404
    except Exception, e:
        raise e

@login_required
@coordinatorOrbossRequired
def getEmailUnique(request):
    try:
        if request.is_ajax() and request and request.method=='GET' and 'user' in request.GET:
            r = re.compile('profesor[0-9]+$')
            if r.match(request.GET['user']) is not None:
                username = request.GET['user'].split('profesor')
                username.remove('')
                return HttpResponse(User.objects.get(username=username[0]).email)
            else:
                print 'Expresion Mal Formada'
                raise Http404
        else:
            raise Http404
    except Exception, e:
        raise e

@login_required
@coordinatorOrbossRequired
def getProfileInfo(request,key):
    try:
        if request.is_ajax() and request and request.method=='GET':
            usrprofile = Usuario.objects.filter(id=int(key)).values('usuario_id__username','usuario_id__email','usuario_id__first_name','usuario_id__last_name','telefono_celular','telefono_oficina','telefono_casa','fecha_ingreso','direccion','dedicacion','estatus','tipo_contrato__nombre')
            castedDates = [{ key : convertDatetimeToString(value) if isinstance(value,datetime.date) else value  for key,value in usrprofile[0].items()}]
            return HttpResponse(json.dumps(castedDates[0]), content_type="application/json")
        else:
            raise Http404
    except Exception, e:
        raise e

@login_required
@coordinatorOrbossRequired
def horario(request,rol):
    try:
        if request:
            usr = Usuario.objects.get(usuario_id = request.user.pk)
            roles = UsuarioRol.objects.filter(cedula=usr)
            return render_to_response('HorarioPlanificacion.html',{'pk':usr.pk,'usuario':request.user.first_name+" "+request.user.last_name,'centro':usr.centro.nombre,'rol':rol, 'roles':roles, 'listaHorarios': [7,8,9,10,11,12,1,2,3,4,5,6]},context_instance=RequestContext(request))
        else:
            raise Http404            
    except Exception, e:
        raise e

@login_required
@bossRequired
def export(request):
    try:
        if request :
            usr = Usuario.objects.get(usuario_id = request.user.pk)
            roles = UsuarioRol.objects.filter(cedula=usr)
            return render_to_response("JD_exportar.html",{'usuario':request.user.first_name+" "+request.user.last_name,'centro':usr.centro.nombre,'pk':usr.pk, 'roles':roles},context_instance=RequestContext(request))
        else:
            raise Http404
    except Exception, e:
        raise e

'''Obtener el horario de solicitudes del sistema'''
@login_required
@coordinatorOrbossRequired
def getScheduleByRequest(request,rol):
    if request.is_ajax() and request and request.method=='GET' :
        rol_pattern = rol.lower()

        if rol_pattern == 'cc':
            try:
                centro = Usuario.objects.get(usuario_id=request.user.pk).centro
                center_schedule_list = HorarioSolicitado.objects.filter(horario_solicitado__usuario__centro=centro).filter(horario_solicitado__estatus__in=['P','AC','RC','PJ','RJ','AJ']).values('hora_inicio','hora_fin', 'dia_semana','horario_solicitado__materia__materia__nombre','horario_solicitado__materia__materia_id','horario_solicitado_id','id', 'horario_solicitado__usuario__usuario_id__username', 'horario_solicitado__usuario__usuario_id__first_name', 'horario_solicitado__usuario__usuario_id__last_name', 'horario_solicitado__estatus', 'horario_solicitado__incomplete_status', 'horario_solicitado__usuario__centro__nombre')
            except Exception, e:
                raise e
        elif  rol_pattern == 'jdd':
            try:
                center_schedule_list = HorarioSolicitado.objects.filter(horario_solicitado__estatus__in=['PJ','AJ','RJ','AC']).values('hora_inicio','hora_fin', 'dia_semana','horario_solicitado__materia__materia__nombre','horario_solicitado__materia__materia_id','horario_solicitado_id','id', 'horario_solicitado__usuario__usuario_id__username', 'horario_solicitado__usuario__usuario_id__first_name', 'horario_solicitado__usuario__usuario_id__last_name', 'horario_solicitado__estatus', 'horario_solicitado__incomplete_status', 'horario_solicitado__usuario__centro__nombre')
            except Exception, e:
                raise e
        else:
            raise Http404

        '''
        Formato Posicional Json de Retorno:
        [0]materia_id, [1]materia_solicitada_id, [2]username ,
        [3]nombre , [4]dia_seman, [5]hora_inicio, [6]hora_fin,
        [7]estatus,[8]descripcion_estatus, [9] incompleto , [10] centro
        '''
        jsontmp = {}
        counter = 0
        for h in center_schedule_list:
            jsontmp.update(
            {
            counter:    
             {
             'materia_id': h['horario_solicitado__materia__materia_id'],
             'materia_solicitada':h['horario_solicitado_id'],
             'horario_solicitado':h['id'],
             'username':h['horario_solicitado__usuario__usuario_id__username'],
			 'usuario':h['horario_solicitado__usuario__usuario_id__first_name']+' '+h['horario_solicitado__usuario__usuario_id__last_name'],
             'nombre':h['horario_solicitado__materia__materia__nombre'],
             'dia_semana':h['dia_semana'],
             'hora_inicio':convertDatetimeToString(h['hora_inicio']),
             'hora_fin':convertDatetimeToString(h['hora_fin']),
             'estatus': h['horario_solicitado__estatus'],
             'descripcion_estatus' : translateStatus(h['horario_solicitado__estatus']),
             'incompleto': 'I' if h['horario_solicitado__incomplete_status'] else '',
             'centro': h['horario_solicitado__usuario__centro__nombre'],
             }
            }
            )
            counter +=1

        jsontmp.update({'length':counter})

        return  HttpResponse(json.dumps(jsontmp,sort_keys=True), content_type="application/json")
    else:
        raise Http404;


'''
Usuarios que realizaron solicitudes de materias de un centro
y que ademas el estatus de su solicitud este dentro de ['P','AC','RC','PJ','RJ','AJ']
'''
@login_required
@coordinatorRequired
def getUserByCenter(request):
    try:
        if request.is_ajax() and request and request.method=='GET' :
            centro = Usuario.objects.get(usuario_id=request.user.pk).centro
            final_user_list = HorarioSolicitado.objects.filter(horario_solicitado__usuario__centro=centro).filter(horario_solicitado__estatus__in=['P','AC','RC','PJ','RJ','AJ']).order_by('horario_solicitado__usuario__usuario_id__first_name','horario_solicitado__usuario__usuario_id__last_name','horario_solicitado__usuario__usuario_id__username').values('horario_solicitado__usuario__usuario_id__username','horario_solicitado__usuario__usuario_id__first_name','horario_solicitado__usuario__usuario_id__last_name')
            name = []
            counter = 0
            jsontemp = {}
            for u in final_user_list:
                if u['horario_solicitado__usuario__usuario_id__first_name']+' '+u['horario_solicitado__usuario__usuario_id__last_name'] not in name:
                    jsontemp.update({
                        counter:{
                        'username':u['horario_solicitado__usuario__usuario_id__username'],
                        'name': u['horario_solicitado__usuario__usuario_id__first_name']+' '+u['horario_solicitado__usuario__usuario_id__last_name']}
                        })
                    counter +=1;
                    name.append(u['horario_solicitado__usuario__usuario_id__first_name']+' '+u['horario_solicitado__usuario__usuario_id__last_name'])            

            jsontemp.update({'length':counter})

            return HttpResponse(json.dumps(jsontemp, sort_keys=True),content_type="application/json")
        else:
            raise Http404        
    except Exception, e:
        raise e
 

'''
Materias solicitadas por usuarios de un centro
que poseen estatus iguales a ['P','AC','RC','PJ','RJ','AJ']
'''
@login_required
@coordinatorRequired
def getSubjectByRequest(request):
    try:
        if request.is_ajax() and request and request.method=='GET' :
            centro = Usuario.objects.get(usuario_id=request.user.pk).centro
            center_request_subject_list=HorarioSolicitado.objects.filter(horario_solicitado__usuario__centro=centro).filter(horario_solicitado__estatus__in=['P','AC','RC','PJ','RJ','AJ']).order_by('horario_solicitado__materia__materia__nombre').values('horario_solicitado__materia__materia__pk','horario_solicitado__materia__materia__nombre')
            jsontemp = {}
            counter = 0
            names = []
            for e in center_request_subject_list:
                if e['horario_solicitado__materia__materia__nombre'] not in names:
                    jsontemp.update({counter:{'id':e['horario_solicitado__materia__materia__pk'],'nombre':e['horario_solicitado__materia__materia__nombre']}})
                    names.append(e['horario_solicitado__materia__materia__nombre'])
                    counter+=1
            
            jsontemp.update({'length':counter})

            return HttpResponse(json.dumps(jsontemp, sort_keys=True),content_type="application/json")       
        else:
            raise Http404
    except Exception, e:
        raise e


'''
Todos los usuarios que realizaron solicitudes de materias
las cuales poseen uno de los siguientes estatus ['PJ','AJ','RJ','AC']
'''
@login_required
@bossRequired
def getUserByCenterAll(request):
    try:
        if request.is_ajax() and request and request.method=='GET' :
            final_user_list = HorarioSolicitado.objects.filter(horario_solicitado__estatus__in=['PJ','AJ','RJ','AC']).order_by('horario_solicitado__usuario__usuario_id__first_name','horario_solicitado__usuario__usuario_id__last_name','horario_solicitado__usuario__usuario_id__username').values('horario_solicitado__usuario__usuario_id__username','horario_solicitado__usuario__usuario_id__first_name','horario_solicitado__usuario__usuario_id__last_name')
            name = []
            counter = 0
            jsontemp = {}
            for u in final_user_list:
                if u['horario_solicitado__usuario__usuario_id__first_name']+' '+u['horario_solicitado__usuario__usuario_id__last_name'] not in name:
                    jsontemp.update({
                        counter:{
                        'username':u['horario_solicitado__usuario__usuario_id__username'],
                        'name': u['horario_solicitado__usuario__usuario_id__first_name']+' '+u['horario_solicitado__usuario__usuario_id__last_name']}
                        })
                    counter +=1;
                    name.append(u['horario_solicitado__usuario__usuario_id__first_name']+' '+u['horario_solicitado__usuario__usuario_id__last_name'])            

            jsontemp.update({'length':counter})

            return HttpResponse(json.dumps(jsontemp, sort_keys=True),content_type="application/json")
        else:
            raise Http404        
    except Exception, e:
        raise e


'''
Todas las materias solicitadas de la escuela
que posee estatus iguales a  ['PJ','AJ','RJ','AC']
'''
@login_required
@bossRequired
def getSubjectByRequestAll(request):
    try:
        if request.is_ajax() and request and request.method=='GET' :
            center_request_subject_list=HorarioSolicitado.objects.filter(horario_solicitado__estatus__in=['PJ','AJ','RJ','AC']).order_by('horario_solicitado__materia__materia__nombre').values('horario_solicitado__materia__materia__pk','horario_solicitado__materia__materia__nombre')
            jsontemp = {}
            counter = 0
            names = []
            for e in center_request_subject_list:
                if e['horario_solicitado__materia__materia__nombre'] not in names:
                    jsontemp.update({counter:{'id':e['horario_solicitado__materia__materia__pk'],'nombre':e['horario_solicitado__materia__materia__nombre']}})
                    names.append(e['horario_solicitado__materia__materia__nombre'])
                    counter+=1
            
            jsontemp.update({'length':counter})

            return HttpResponse(json.dumps(jsontemp, sort_keys=True),content_type="application/json")       
        else:
            raise Http404
    except Exception, e:
        raise e

@login_required
@bossRequired
def getChartData(request):
    try:
        if request and request.is_ajax() and request.method == 'POST':
            centros = Centro.objects.all().values_list('nombre',flat=True)
            remCounters = {}
            i = 0
            for c in centros:
                remCounters.update({
                    i:{'name':c,'remaining':len(HorarioSolicitado.objects.filter(horario_solicitado__usuario__centro__nombre=c).filter(horario_solicitado__estatus__in=['N']).values_list('horario_solicitado__usuario__usuario_id__username',flat=True).distinct())}   
                })
                i+=1
            remCounters.update({'length':i})
            return HttpResponse(json.dumps(remCounters, sort_keys=True),content_type="application/json")       
        else:
            raise Http404
    except Exception, e:
        raise e

'''
Cambio de estatus para las solicitudes, realiza el cambio de estatus de una 
lista de solicitudes data: Es recibido en el POST, un json de la forma 
{id_materia_solicitada:new_estatus} id_materia_solicitada es el id 
de la materia solicitada y estatus es nuevo estatus para esa solicitud
'''
@login_required
def ChangeStatus(request):
    try:
        if request and request.is_ajax() and request.method == 'POST' and 'data' in request.POST:
            if(len(request.POST['data'])):
                data = json.loads(request.POST['data'])
                remaining = 0
                
                # Si el CC envia su rol, entonces se calcula el numero de participante 
                # que faltan por enviar su propuesta.
                if 'rol' in data:
                    if data['rol'].lower() == 'cc':
                        del data['rol']
                        centro = centro = Usuario.objects.get(usuario_id=request.user.pk).centro
                        remaining = len(HorarioSolicitado.objects.filter(horario_solicitado__usuario__centro=centro).filter(horario_solicitado__estatus__in=['N']).values_list('horario_solicitado__usuario__usuario_id__username',flat=True).distinct())

                materias = MateriaSolicitada.objects.select_for_update().filter(id__in = [ int(e) for e in data.keys() ])
                for i in xrange(len(materias)):
                    materias[i].estatus = data[str(materias[i].id)]
                    materias[i].incomplete_status = True if remaining > 0 else False;
                    materias[i].save()
                
                return HttpResponse(remaining,status=200)
            else:
                raise Http404
        else:
            raise Http404
    except Exception, e:
        raise e

#Export CSV
def programacionFormatoCSV(request):
    #Creamos el objeto Httpresponse con la cabecera csv apropiada.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="programacion.csv"'

    #Creamos un escritor csv usando httpResponse como "archivo"
    listaMaterias = Materia.objects.all()
    writer = csv.writer(response)
    writer.writerow(['Codigo', 'Nombre', 'Tipo de Materia'])

    try:
        pass
        #for (materia) in listaMaterias: 
        #    writer.writerow([materia.codigo, materia.nombre, materia.tipo_materia])
        #return response
    except csv.error as e:
        pass
        #sys.exit('file %s, line ')
    

