#encoding:utf-8
from django.db.models.loading import get_app, get_models, get_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.test.client import Client
from principal.manager import entity
from django.test import TestCase
from principal.models import *
from datetime import datetime
from principal.forms import *
from django import forms
from random import *
import sys

# Generadores aleatorios para pruebas unitarias #
#################################################

class RandomGenerator(object):
	seed()
	ascii_letters_set = map ((lambda i : unichr(i)),range(97,123)) + map ((lambda i : unichr(i)),range(65,91)) + [u'ñ']
	extended_ascii_set = map ((lambda i : unichr(i)),range(33,240))
	maxInt = sys.maxint
	minInt = -sys.maxint
	maxyear =  datetime.now().year + 1000
	validEmailset = ['niceandsimple@example.com','very.common@example.com','a.little.lengthy.but.fine@dept.example.com', 'disposable.style.email.with+symbol@example.com', '"very.unusual.@.unusual.com"@example.com']
	invalidEmailset =  ['Abc.example.com','A@b@c@example.com' ,'a"b(c)d,e:f;g<h>i[j\k]l@example.com','just"not"right@example.com','this is"not\\allowed@example.com','this\ still\"not\\allowed@example.com']
	
	'''
		- genRandomString -
		Funcion generadora de cadenas de caracteres aleatorios,
		
		weird (opcional): colocando weird = True se genera una 
		cadena con caracteres pertenecientes a la tabla ascii extendido
		en caso contrario la cadena de caracteres sigue la tabla ascii.

		especific_long (opcional) : especifica la longitud que debe tener 
		el string generado.

		max_long (opcional) : si especific_long no es suministrado
		se toma entonces el valor de max_long. 
	'''
	@classmethod
	def genRandomString(self,weird = False, especific_long = None, max_long = 1000):
		string = ''
		l = (len(self.ascii_letters_set) if not weird else len(self.extended_ascii_set))-1
		set = self.ascii_letters_set if not weird else self.extended_ascii_set
		long = randint(1, max_long) if especific_long is None else especific_long
		while long:
			string += set[randint(0,l)]
			long-=1
		return string

	'''
		- genRandomInteger -
		valid (opcional) : valid = True sugiere que los valores enteros 
		generados seran enteros positivos.

		max/min_value (opcional): permiten especificar si el valor generado 
		pertenece a determinado rango donde siendo x el valor generado
		min_value <= x <=max_value
	'''
	@classmethod
	def genRandomInteger(self,valid=True, max_value = None, min_value = None):
		return (randint(0,self.maxInt) if max_value is None or min_value is None else randint(min_value,max_value) ) if valid else randint(self.minInt,-1)

	'''
		- genRandomDate -
		valid (opcional): valid = True permite determinar si la 
		fecha generada sera valida o no.

		separator (opcional): si no es suministrado se genera una fecha
		vacia, en caso contrario este valor debe ser un caracter denotando
		el separador a ser usado en la fecha generada.
	'''
	@classmethod
	def genRandomDate(self,valid=True, separator=None):

		date = ''
		if separator or len(separator)!= 1:			
			if valid :
				year = randint(1958, datetime.now().year)
				month = randint(1, 12)
				day = randint(1, 31) if month in [1,5,7,8,10,12] else (randint(1, 30) if month != 2 else 28)
			else:
				year = randint(datetime.now().year+1,self.maxyear)
				month = randint(13, 70)
				day = randint(32, 70)
			date = str(day)+separator+str(month)+separator+str(year)
		return date

	'''
		-genRandomTime-
		valid (opcional): valid = True , sugiere generacion
		de horas validas, en formato de 24 horas.
	'''
	@classmethod
	def genRandomTime(self,valid=True):

		min_hour = 0 if valid else -30
		max_hour = 23 if valid else 53
		min_minutes = 0 if valid else -30
		max_minutes = 59 if valid else 89
		m = randint(min_minutes, max_minutes)

		hours = "%02d" % (randint(min_hour,max_hour))
		minutes =  "%02d" % m if m>0 else ( "-%02d" % -m if m<=0 and m >=-9 else "%02d" % m)

		return hours+':'+minutes

	'''
		-genEmail-
		empty (opcional): permite generar Email vacio.

		valid(opcional): permite la generacion de email valido si
		es suministrado como True, los emails tomados como casos de prueba
		son atributos de la clase generadora.
	'''
	@classmethod
	def genEmail(self,valid=True, empty = False):
		email = ''
		if not empty:
			if valid :
				email = self.validEmailset[randint(0,len(self.validEmailset)-1)]			
			else:			
				email = self.invalidEmailset[randint(0,len(self.invalidEmailset)-1)]
		
		return email

# Metodos para generar formularios de prueba #
##############################################

def templateForm( type_id,  excludes=None):
	class _ObjectForm( forms.ModelForm ):
		class Meta:
			model = ContentType.objects.get( pk=type_id ).model_class() 
	return _ObjectForm

class FormFactory():
	@classmethod
	def genForm(self,modelo,inst):
		type_id = ContentType.objects.get_for_model(get_model('principal',str(modelo).replace(' ',''))).id
		if modelo == 'usuario':
			return CustomUserForm(False, inst.toJson(False))
		else:
			form_class = templateForm(type_id)
			return form_class(inst.toJson(False))

# Pruebas unitarias sobre los siguientes modelos: #
# TipoDocente                                     #
# JerarquiaDocente                                #
# Usuario                                         #
# Materia                                         #
# HorarioMateria                                  #
# Programacion                                    #
#                                                 #
# - Pruebas FrontEnd:                             #
# Se toma un field de cada tipo en cada modelo    #
# y se realizan las pruebas de correctitud        #
#                                                 #
# - Pruebas BackEnd:                              #
# Se realizan pruebas de insercion, eliminacion   #
# y actualizacion                                 #
###################################################

class GlobalValidationTest(TestCase):
	pass

class TipoDocenteTest(TestCase):
	def setUp(self):
		# Setting up a fake user logged-in
		u = User(username='test')
		u.set_password('0000')
		u.save()
		self.main_client = Client()
		self.main_client.login(username='test', password='0000')

	#Pruebas Frontend
	def test_NormalShortName(self):
		model_object = TipoDocente(nombre = RandomGenerator.genRandomString(especific_long=50))
		form = FormFactory.genForm('tipo docente',model_object)
		self.assertTrue(form.is_valid())	

	def test_inputToLongNormalName(self):
		model_object = TipoDocente(nombre = RandomGenerator.genRandomString(especific_long=150))
		form = FormFactory.genForm('tipo docente',model_object)
		self.assertTrue(not form.is_valid())

	def test_inputWeirdShortName(self):
		model_object = TipoDocente(nombre = RandomGenerator.genRandomString(weird=True,especific_long=50))
		form = FormFactory.genForm('tipo docente',model_object)
		self.assertTrue(form.is_valid())
	
	def test_inputWeirdToLongName(self):
		model_object = TipoDocente(nombre = RandomGenerator.genRandomString(weird=True,especific_long=150))
		form = FormFactory.genForm('tipo docente',model_object)
		self.assertTrue(not form.is_valid())

	def test_inputEmptyName(self):
		model_object = TipoDocente(nombre = '')
		form = FormFactory.genForm('tipo docente',model_object)
		self.assertTrue(not form.is_valid())

	#Pruebas Backend
	def test_create(self):
		self.assertEqual(len(TipoDocente.objects.all()),0)
		response =  self.main_client.post('/admins/modelos/tipo docente/crear', {'nombre': 'abc'})
		self.assertEqual(response.status_code,302)#Redirectioning to another template
		self.assertEqual(len(TipoDocente.objects.all()),1)

	def test_delete(self):
		self.assertEqual(len(TipoDocente.objects.all()),0)		
		l = len(TipoDocente.objects.all())
		temp = TipoDocente(nombre='abc')
		temp.save()
		self.assertEqual(len(TipoDocente.objects.all()),1)
		response = self.main_client.post('/admins/modelos/tipo docente/borrar/'+str(temp.pk))
		self.assertEqual(response.status_code,302)#Redirectioning to another template
		self.assertEqual(len(TipoDocente.objects.all()),0)

	def test_update(self):
		self.assertEqual(len(TipoDocente.objects.all()),0)	
		temp = TipoDocente.objects.create(nombre='abc')
		self.assertEqual(len(TipoDocente.objects.all()),1)	
		pkey = temp.pk
		old = temp.nombre
		response = self.main_client.post('/admins/modelos/tipo docente/editar/'+str(temp.pk),{'nombre':'cba'})
		self.assertEqual(response.status_code,302)#Redirectioning to another template
		temp = TipoDocente.objects.get(pk=pkey)
		self.assertTrue(old != temp.nombre)


class JerarquiaDocenteTest(TestCase):	
	def setUp(self):
		# Setting up a fake user logged-in
		u = User(username='test')
		u.set_password('0000')
		u.save()
		self.main_client = Client()
		self.main_client.login(username='test', password='0000')
		self.tipoDocente = TipoDocente.objects.create(pk=1,nombre='xtipo')

	#Pruebas Frontend
	def test_inputInvalidJerarquia(self):
		model_object = JerarquiaDocente(jerarquia = RandomGenerator.genRandomInteger(valid=False),
		nombre= 'abc',tipo_docente_id = 1)
		form = FormFactory.genForm('jerarquia docente',model_object)
		self.assertTrue(not form.is_valid())

	def test_inputWeirdToLongName(self):
		model_object = JerarquiaDocente(
			jerarquia = 6,
			nombre=  RandomGenerator.genRandomString(weird=True,especific_long=150),
			tipo_docente_id = 1)
		form = FormFactory.genForm('jerarquia docente',model_object)
		self.assertTrue(not form.is_valid())

	def test_inputEmptyName(self):
		model_object = JerarquiaDocente(
			jerarquia = 6,
			nombre=  '',
			tipo_docente_id = 1)
		form = FormFactory.genForm('jerarquia docente',model_object)
		self.assertTrue(not form.is_valid())

	def test_inputToLongNormalName(self):
		model_object = JerarquiaDocente(
			jerarquia = 6,
			nombre=  RandomGenerator.genRandomString(especific_long=150),
			tipo_docente_id = 1)
		form = FormFactory.genForm('jerarquia docente',model_object)
		self.assertTrue(not form.is_valid())

	def test_NormalShortName(self):
		model_object = JerarquiaDocente(
			jerarquia = 6,
			nombre= 'abc',
			tipo_docente_id = 1)
		form = FormFactory.genForm('jerarquia docente',model_object)
		self.assertTrue(form.is_valid())

	#Pruebas Backend
	def test_create(self):
		self.assertEqual(len(JerarquiaDocente.objects.all()),0)
		response =  self.main_client.post('/admins/modelos/jerarquia docente/crear', {'jerarquia':1, 'nombre': 'abc','tipo_docente':1})
		self.assertEqual(response.status_code,302)#Redirectioning to another template
		self.assertEqual(len(JerarquiaDocente.objects.all()),1)

	def test_delete(self):
		self.assertEqual(len(JerarquiaDocente.objects.all()),0)		
		model_object = JerarquiaDocente.objects.create(
			jerarquia = 6,
			nombre=  'abc',
			tipo_docente_id = 1)
		self.assertEqual(len(JerarquiaDocente.objects.all()),1)
		response = self.main_client.post('/admins/modelos/jerarquia docente/borrar/'+str(model_object.pk))
		self.assertEqual(response.status_code,302)#Redirectioning to another template
		self.assertEqual(len(JerarquiaDocente.objects.all()),0)

	def test_update(self):
		self.assertEqual(len(JerarquiaDocente.objects.all()),0)	
		model_object = JerarquiaDocente.objects.create(
			jerarquia = 6,
			nombre=  'abc',
			tipo_docente_id = 1)
		self.assertEqual(len(JerarquiaDocente.objects.all()),1)
		pkey = model_object.pk
		old = (model_object.nombre,model_object.jerarquia,model_object.tipo_docente)
		response = self.main_client.post('/admins/modelos/jerarquia docente/editar/'+str(model_object.pk),{'jerarquia':1,'nombre':'cba','tipo_docente':1})
		temp = JerarquiaDocente.objects.get(pk=pkey)
		self.assertTrue(old != (temp.nombre,temp.jerarquia,temp.tipo_docente))


class UsuarioTest(TestCase):
	def setUp(self):
		# Setting up a fake user logged-in
		self.u = User(pk=1,username='123456',first_name='test',last_name='test',email='example@domain.com')
		self.u.set_password('0000')
		self.u.save()
		self.main_client = Client()
		self.main_client.login(username='123456', password='0000')

		self.tipoDocente = TipoDocente.objects.create(pk=1,nombre='xtipo')
		self.jerarquiaDocente = JerarquiaDocente.objects.create(pk=1,jerarquia=1,nombre='xjerarquia',tipo_docente_id=1)
		self.tipoContrato = TipoContrato.objects.create(pk=1,nombre='xtipo')
		self.Centro = Centro.objects.create(pk=1,nombre='xcentro', area='any')

	#Pruebas Frontend
	def test_inputInvalidDate(self):
		model_object = Usuario(
			usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = '123456',
			fecha_ingreso = RandomGenerator.genRandomDate(valid=False,separator='/'),
			direccion = '',	dedicacion = '6 hrs', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)

		form = FormFactory.genForm('usuario',model_object)
		self.assertTrue(not form.is_valid())

	def test_NormalRandomShortPhone(self):
		model_object = Usuario(
			usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = RandomGenerator.genRandomString(especific_long=20),
			fecha_ingreso = '1/1/2013',
			direccion = '',	dedicacion = '6 hrs', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)

		form = FormFactory.genForm('usuario',model_object)
		self.assertTrue(form.is_valid())

	def test_NormalRandomToLongPhone(self):
		model_object = Usuario(
			usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = RandomGenerator.genRandomString(especific_long=21),
			fecha_ingreso = '1/1/2013',
			direccion = '',	dedicacion = '6 hrs', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)

		form = FormFactory.genForm('usuario',model_object)
		self.assertTrue(not form.is_valid())

	def test_EmptyDate(self):
		model_object = Usuario(
			usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa ='123456',
			fecha_ingreso = '',
			direccion = '',	dedicacion = '6 hrs', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)

		form = FormFactory.genForm('usuario',model_object)
		self.assertTrue(not form.is_valid())

	def test_InvalidEmail(self):
		self.u.email= RandomGenerator.genEmail(valid=False)
		self.u.save()
		model_object = Usuario(
			usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = '123456',
			fecha_ingreso = '1/1/2013',
			direccion = '',	dedicacion = '6 hrs', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)

		form = FormFactory.genForm('usuario',model_object)
		self.assertTrue(not form.is_valid())

	def test_emptyEstatus(self):
		model_object = Usuario(
			usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = '123456',
			fecha_ingreso = '1/1/2013',
			direccion = '',	dedicacion = '6 hrs', estatus = '',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)

		form = FormFactory.genForm('usuario',model_object)
		self.assertTrue(not form.is_valid())

	def test_emptyDedicacion(self):
		model_object = Usuario(
			usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = '123456',
			fecha_ingreso = '1/1/2013',
			direccion = '',	dedicacion = '', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)

		form = FormFactory.genForm('usuario',model_object)
		self.assertTrue(not form.is_valid())

	#Pruebas Backend
	def test_createUniqueUser(self):

		self.assertEqual(Usuario.objects.count(),0)
		response =  self.main_client.post('/admins/modelos/usuario/crear', 
		{'usuario_id' :'123457','nombre' : 'test','apellido' : 'test', 'password' : '1234',
		'correo_Electronico' : 'example@domain.com' ,'telefono_celular' : '123456',
		'telefono_oficina' : '123456','telefono_casa' : '12356','fecha_ingreso' : '1/1/2013',	'direccion' : '',
		'dedicacion' : '6 hrs','estatus' : 'A',	'jerarquia_docente' : 1, 'tipo_contrato' : 1,'centro' : 1})
		self.assertEqual(response.status_code,302)
		self.assertEqual(Usuario.objects.count(),1)

#Pruebas sobre Usuario_Rol

class AulaTestCases(TestCase):

    def setUp(self):
        self.a = Aula(tipo_aula='I',capacidad=30,estatus_aula='A')
        self.a.save()
        self.u = User.objects.create_user(username='brucewayne', email='batman@gmail.com', password='batman')



    def test_InsertarAula(self):
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula/crear")
        self.assertEqual(response.status_code,200)

    def test_EditarAula(self):
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula/editar/"+str(self.a.pk))
        self.assertEqual(response.status_code,200)

    def test_BorrarAula(self):
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula/borrar/"+str(self.a.pk))
        self.assertRedirects(response,"/admins/modelos/aula",302,200)

    def test_ListarAula(self):
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula")
        self.assertEqual(response.status_code,200)

    def test_LeerAula(self):
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula/"+str(self.a.pk))
        self.assertEqual(response.status_code,200)



    def test_InsertarAulaSinLogin(self):
        response = self.client.post("/admins/modelos/aula/crear")
        self.assertRedirects(response,"/login?next=/admins/modelos/aula/crear",302,200)

    def test_EditarAulaSinLogin(self):
        response = self.client.post("/admins/modelos/aula/editar/"+str(self.a.pk))
        self.assertRedirects(response,"/login?next=/admins/modelos/aula/editar/"+str(self.a.pk),302,200)

    def test_BorrarAulaSinLogin(self):
        response = self.client.post("/admins/modelos/aula/borrar/"+str(self.a.pk))
        self.assertRedirects(response,"/login?next=/admins/modelos/aula/borrar/"+str(self.a.pk),302,200)

    def test_ListarAulaSinLogin(self):
        response = self.client.post("/admins/modelos/aula")
        self.assertRedirects(response,"/login?next=/admins/modelos/aula",302,200)

    def test_LeerAulaSinLogin(self):
        response = self.client.post("/admins/modelos/aula/"+str(self.a.pk))
        self.assertRedirects(response,"/login?next=/admins/modelos/aula/"+str(self.a.pk),302,200)

class NotificacionTest(TestCase):
	def setUp(self):
		self.u = User.objects.create_user(pk=1,username='brucewayne', email='batman@gmail.com', password='batman')
		self.u = User.objects.create_user(pk=2,username='peterparker', email='spiderman@gmail.com', password='spiderman')
		self.tipoDocente = TipoDocente.objects.create(pk=1,nombre='xtipo')
		self.jerarquiaDocente = JerarquiaDocente.objects.create(pk=1,jerarquia=1,nombre='xjerarquia',tipo_docente_id=1)
		self.tipoContrato = TipoContrato.objects.create(pk=1,nombre='xtipo')
		self.Centro = Centro.objects.create(pk=1,nombre='xcentro', area='any')
		self.usuarioE = Usuario.objects.create(pk=1,usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = '123456',
			fecha_ingreso = '2013-1-1',
			direccion = '',	dedicacion = '6 hrs', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)
		self.usuarioR = Usuario.objects.create(pk=2,usuario_id_id=2,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = '123456',
			fecha_ingreso = '2013-1-1',
			direccion = '',	dedicacion = '6 hrs', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)
		self.notificacion = Notificacion(fecha = '2013-1-4', asunto = 'wgejf' , contenido = 'gsdjgdsaf' , estatus = 'as' , usuario_emisor = self.usuarioE , usuario_receptor = self.usuarioR)
		self.notificacion.save()

	def normalTest(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = Notificacion(fecha = '2013-1-4', asunto = 'wgejf' , contenido = 'gsdjgdsaf' , estatus = 'astdfjhsagdfha' , usuario_emisor = self.usuarioE , usuario_receptor = self.usuarioR)
		form = FormFactory.genForm('notificacion' , model_object)
		self.assertEqual(True,form.is_valid())

	def tooLongAsunto(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = Notificacion(fecha = 'wrenj', asunto = RandomGenerator.genRandomString(especific_long=150) , contenido = 'gsdjgdsaf' , estatus = 'agsd' , usuario_emisor = self.usuarioE , usuario_receptor = self.usuarioR)
		form = FormFactory.genForm('notificacion' , model_object)
		self.assertEqual(False,form.is_valid())

	def test_UpdateNotificacion(self):
		self.client.login(username='brucewayne',password='batman')
		self.assertEqual(Notificacion.objects.count(),1)		
		asunto = self.notificacion.asunto
		pkey = self.notificacion.pk
		response = self.client.post("/admins/modelos/notificacion/editar/"+str(self.notificacion.pk), {'fecha': 'wrenj' , 'asunto': 'NEW SUBJECT', 'contenido': 'gsdjgdsaf','estatus' : 'agsd' , 'usuario_emisor ': self.usuarioE, 'usuario_receptor ' : self.usuarioR })
		self.assertEqual(response.status_code,200)
		new_subject = Notificacion.objects.get(pk=pkey).asunto
		print 'asunto: ' + asunto
		print 'new_subject: '+ new_subject
		self.assertTrue(asunto != new_subject)


	def test_LeerNotificacion(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/notificacion/"+str(self.notificacion.pk))
		self.assertEqual(response.status_code,200)

	def test_EditarNotificacion(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/notificacion/editar/"+str(self.notificacion.pk))
		self.assertEqual(response.status_code,200)

	def test_BorrarNotificacion(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/notificacion/borrar/"+str(self.notificacion.pk))
		self.assertEqual(response.status_code,200)	

	def test_CrearNotificacion(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/notificacion/crear")
		self.assertEqual(response.status_code,200)

class UsuarioRolTest(TestCase):
	def setUp(self):
		self.u = User.objects.create_user(pk=1,username='brucewayne', email='batman@gmail.com', password='batman')
		self.u = User.objects.create_user(pk=2,username='peterparker', email='spiderman@gmail.com', password='spiderman')
		self.tipoDocente = TipoDocente.objects.create(pk=1,nombre='xtipo')
		self.jerarquiaDocente = JerarquiaDocente.objects.create(pk=1,jerarquia=1,nombre='xjerarquia',tipo_docente_id=1)
		self.tipoContrato = TipoContrato.objects.create(pk=1,nombre='xtipo')
		self.Centro = Centro.objects.create(pk=1,nombre='xcentro', area='any')
		self.rol = Rol.objects.create(pk=1, rol_id=1, nombre = 'sghdsjaf', descripcion = 'sghadashfd')
		self.usuario = Usuario.objects.create(pk=1,usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = '123456',
			fecha_ingreso = '2013-1-1',
			direccion = '',	dedicacion = '6 hrs', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)
		self.UsuarioRol = UsuarioRol(rol_id=1,cedula = self.usuario)
		self.UsuarioRol.save()
		

	def normalTest(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = UsuarioRol(rol_id=1, cedula = self.usuario)
		form = FormFactory.genForm('usuario rol' , model_object)
		self.assertEqual(True, form.is_valid())

	def test_LeerUsuarioRol(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/UsuarioRol/"+str(self.UsuarioRol.pk))
		self.assertEqual(response.status_code,200)

	def test_EditarUsuarioRol(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/UsuarioRol/editar/"+str(self.UsuarioRol.pk))
		self.assertEqual(response.status_code,200)

	def test_BorrarUsuarioRol(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/UsuarioRol/borrar/"+str(self.UsuarioRol.pk))
		self.assertEqual(response.status_code,200)	

	def test_CrearUsuarioRol(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/UsuarioRol/crear")
		self.assertEqual(response.status_code,200)

class HorarioSolicitadoTest(TestCase):
	def setUp(self):
		self.u = User.objects.create_user(pk=1,username='brucewayne', email='batman@gmail.com', password='batman')
		self.tipoDocente = TipoDocente.objects.create(pk=1,nombre='xtipo')
		self.jerarquiaDocente = JerarquiaDocente.objects.create(pk=1,jerarquia=1,nombre='xjerarquia',tipo_docente_id=1)
		self.tipoContrato = TipoContrato.objects.create(pk=1,nombre='xtipo')
		self.Centro = Centro.objects.create(pk=1,nombre='xcentro', area='any')
		self.rol = Rol.objects.create(pk=1, rol_id=1, nombre = 'sghdsjaf', descripcion = 'sghadashfd')
		self.usuario = Usuario.objects.create(pk=1,usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = '123456',
			fecha_ingreso = '2013-1-1',
			direccion = '',	dedicacion = '6 hrs', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)
		self.aula = Aula.objects.create(aula_id=1,tipo_aula='I',capacidad=30,estatus_aula='A')
		self.periodo_academico = PeriodoAcademico.objects.create(periodo_lectivo = 2013, semestre=2, fecha_inicio='2013-9-16', fecha_fin='2013-11-11')
		self.materia = Materia.objects.create(codigo=6602,
		nombre = 'xnombre', tipo_materia = 'Laboratorio',
		unidades_credito_teoria =2 ,unidades_credito_practica = 2,
		unidades_credito_laboratorio =2 , estatus = 'A',
		semestre = 2013, centro_id = 1)
		self.materiaOfertada = MateriaOfertada.objects.create(nro_estudiantes_estimados=40,nro_secciones_teoria=2,nro_secciones_practica=2,
			nro_secciones_laboratorio=2,nro_preparadores1=2,nro_preparadores2=0, nro_estudiantes_inscritos=30, periodo_academico= self.periodo_academico, materia = self.materia)
		self.materiaSolicitada = MateriaSolicitada.objects.create(estatus='A', usuario=self.usuario, materia=self.materiaOfertada)
		self.horarioS = HorarioSolicitado(dia_semana='Lunes',hora_inicio='7:00',hora_fin='9:00', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		self.horarioS.save()

	def normalCase(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='Lunes',hora_inicio='7:00',hora_fin='9:00', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(True,form.is_valid())

	def wrongDiaSemana(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='dfsasuth',hora_inicio='7:00',hora_fin='9:00', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(False,form.is_valid())

	def wrongHoraInicio(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='Lunes',hora_inicio='30:00',hora_fin='9:00', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(False,form.is_valid())

	def invalidHoraInicio(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='Lunes',hora_inicio='astdfjhsagdfha',hora_fin='9:00', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(False,form.is_valid())

	def wrongFormatHoraInicio(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='Lunes',hora_inicio='7>00',hora_fin='9:00', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(False,form.is_valid())

	def wrongFormatHoraFin(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='Lunes',hora_inicio='7:00',hora_fin='9/00', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(False,form.is_valid())

	def wrongHoraFin(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='Lunes',hora_inicio='7:00',hora_fin='90:00', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(False,form.is_valid())

	def invalidHoraFin(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='Lunes',hora_inicio='7:00',hora_fin='asfd', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(False,form.is_valid())

	def emptyDiaSemana(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='',hora_inicio='7:00',hora_fin='asfd', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(False,form.is_valid())

	def emptyHoraInicio(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='Lunes',hora_inicio='',hora_fin='asfd', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(False,form.is_valid())

	def emptyHoraFin(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = HorarioSolicitado(dia_semana='Martes',hora_inicio='7:00',hora_fin='', horario_solicitado = self.materiaSolicitada , aula = self.aula)
		form = FormFactory.genForm('horario solicitado' , model_object)
		self.assertEqual(False,form.is_valid())

	def test_LeerHorarioSolicitado(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/HorarioSolicitado/"+str(self.horarioS.pk))
		self.assertEqual(response.status_code,200)

	def test_EditarHorarioSolicitado(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/HorarioSolicitado/editar/"+str(self.horarioS.pk))
		self.assertEqual(response.status_code,200)

	def test_BorrarHorarioSolicitado(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/HorarioSolicitado/borrar/"+str(self.horarioS.pk))
		self.assertEqual(response.status_code,200)	

	def test_CrearHorarioSolicitado(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/HorarioSolicitado/crear")
		self.assertEqual(response.status_code,200)

class MateriaOfertadaTest(TestCase):
	def setUp(self):
		self.u = User.objects.create_user(pk=1,username='brucewayne', email='batman@gmail.com', password='batman')
		self.Centro = Centro.objects.create(pk=1,nombre='xcentro', area='any')
		self.materia = Materia.objects.create(codigo=6602,
		nombre = 'xnombre', tipo_materia = 'Laboratorio',
		unidades_credito_teoria =2 ,unidades_credito_practica = 2,
		unidades_credito_laboratorio =2 , estatus = 'A',
		semestre = 2013, centro_id = 1)
		self.periodo_academico = PeriodoAcademico.objects.create(periodo_lectivo = 2013, semestre=2, fecha_inicio='2013-9-16', fecha_fin='2013-11-11')
		self.materiaO = model_object = MateriaOfertada(nro_estudiantes_estimados=40,nro_secciones_teoria=2,nro_secciones_practica=2,nro_secciones_laboratorio=2,nro_preparadores1=2,nro_preparadores2=0, 
			nro_estudiantes_inscritos=30, periodo_academico= self.periodo_academico, materia = self.materia)
		self.materiaO.save()

	def normalCase(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = MateriaOfertada(nro_estudiantes_estimados=40,nro_secciones_teoria=2,nro_secciones_practica=2,nro_secciones_laboratorio=2,nro_preparadores1=2,nro_preparadores2=0, 
			nro_estudiantes_inscritos=30, periodo_academico= self.periodo_academico, materia = self.materia)
		form = FormFactory.genForm('materia ofertada' , model_object)
		self.assertEqual(True,form.is_valid())

	def negativeNroEstudiantes(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = MateriaOfertada(nro_estudiantes_estimados=-40,nro_secciones_teoria=2,nro_secciones_practica=2,nro_secciones_laboratorio=2,nro_preparadores1=2,nro_preparadores2=0, 
			nro_estudiantes_inscritos=30, periodo_academico= self.periodo_academico, materia = self.materia)
		form = FormFactory.genForm('materia ofertada' , model_object)
		self.assertEqual(False,form.is_valid())

	def invalidNroEstudiantes(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = MateriaOfertada(nro_estudiantes_estimados='asfd',nro_secciones_teoria=2,nro_secciones_practica=2,nro_secciones_laboratorio=2,nro_preparadores1=2,nro_preparadores2=0, 
			nro_estudiantes_inscritos=30, periodo_academico= self.periodo_academico, materia = self.materia)
		form = FormFactory.genForm('materia ofertada' , model_object)
		self.assertEqual(False,form.is_valid())

	def test_LeerMateriaOfertada(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/MateriaOfertada/"+str(self.materiaO.pk))
		self.assertEqual(response.status_code,200)

	def test_EditarMateriaOfertada(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/MateriaOfertada/editar/"+str(self.materiaO.pk))
		self.assertEqual(response.status_code,200)

	def test_BorrarMateriaOfertada(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/MateriaOfertada/borrar/"+str(self.materiaO.pk))
		self.assertEqual(response.status_code,200)	

	def test_CrearMateriaOfertada(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/MateriaOfertada/crear")
		self.assertEqual(response.status_code,200)

class MateriaSolicitadaTest(TestCase):
	def setUp(self):
		self.u = User.objects.create_user(pk=1,username='brucewayne', email='batman@gmail.com', password='batman')
		self.tipoDocente = TipoDocente.objects.create(pk=1,nombre='xtipo')
		self.jerarquiaDocente = JerarquiaDocente.objects.create(pk=1,jerarquia=1,nombre='xjerarquia',tipo_docente_id=1)
		self.tipoContrato = TipoContrato.objects.create(pk=1,nombre='xtipo')
		self.Centro = Centro.objects.create(pk=1,nombre='xcentro', area='any')
		self.rol = Rol.objects.create(pk=1, rol_id=1, nombre = 'sghdsjaf', descripcion = 'sghadashfd')
		self.usuario = Usuario.objects.create(pk=1,usuario_id_id=1,telefono_celular = '123456',telefono_oficina = '123456',telefono_casa = '123456',
			fecha_ingreso = '2013-1-1',
			direccion = '',	dedicacion = '6 hrs', estatus = 'A',
			jerarquia_docente_id = 1,tipo_contrato_id = 1,centro_id = 1)
		self.aula = Aula.objects.create(aula_id=1,tipo_aula='I',capacidad=30,estatus_aula='A')
		self.periodo_academico = PeriodoAcademico.objects.create(periodo_lectivo = 2013, semestre=2, fecha_inicio='2013-9-16', fecha_fin='2013-11-11')
		self.materia = Materia.objects.create(codigo=6602,
		nombre = 'xnombre', tipo_materia = 'Laboratorio',
		unidades_credito_teoria =2 ,unidades_credito_practica = 2,
		unidades_credito_laboratorio =2 , estatus = 'A',
		semestre = 2013, centro_id = 1)
		self.materiaOfertada = MateriaOfertada.objects.create(nro_estudiantes_estimados=40,nro_secciones_teoria=2,nro_secciones_practica=2,
			nro_secciones_laboratorio=2,nro_preparadores1=2,nro_preparadores2=0, nro_estudiantes_inscritos=30, periodo_academico= self.periodo_academico, materia = self.materia)
		self.materiaS = MateriaSolicitada( estatus='A', usuario = self.usuario, materia = self.materiaOfertada)
		self.materiaS.save()

	def normalCase(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = MateriaSolicitada( estatus='A', usuario = self.usuario, materia = self.materiaOfertada)
		form = FormFactory.genForm('materia solicitada' , model_object)
		self.assertEqual(True,form.is_valid())

	def wrongEstatus(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = MateriaSolicitada( estatus=17845, usuario = self.usuario, materia = self.materiaOfertada)
		form = FormFactory.genForm('materia solicitada' , model_object)
		self.assertEqual(False,form.is_valid())

	def emptyEstatus(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = MateriaSolicitada( estatus='', usuario = self.usuario, materia = self.materiaOfertada)
		form = FormFactory.genForm('materia solicitada' , model_object)
		self.assertEqual(False,form.is_valid())

	def notValidEstatus(self):
		self.client.login(username='brucewayne',password='batman')
		model_object = MateriaSolicitada( estatus='Q', usuario = self.usuario, materia = self.materiaOfertada)
		form = FormFactory.genForm('materia solicitada' , model_object)
		self.assertEqual(False,form.is_valid())

	def test_LeerMateriaSolicitada(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/MateriaSolicitada/"+str(self.materiaS.pk))
		self.assertEqual(response.status_code,200)

	def test_EditarMateriaSolicitada(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/MateriaSolicitada/editar/"+str(self.materiaS.pk))
		self.assertEqual(response.status_code,200)

	def test_BorrarMateriaSolicitada(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/MateriaSolicitada/borrar/"+str(self.materiaS.pk))
		self.assertEqual(response.status_code,200)	

	def test_CrearMateriaSolicitada(self):
		self.client.login(username='brucewayne',password='batman')
		response = self.client.post("/admins/modelos/MateriaSolicitada/crear")
		self.assertEqual(response.status_code,200)