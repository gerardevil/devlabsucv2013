#encoding:utf-8
from django.db.models.loading import get_app, get_models, get_model
from django.contrib.contenttypes.models import ContentType
from django.test.client import RequestFactory
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
				day = randint(1, 31) if month in [1,5,7,8,10,12] else (randint(1, 30) if month != 2 else randint(1,28))
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

		min_hour = 0 if valid else 24
		max_hour = 23 if valid else 53
		min_minutes = 0 if valid else 60
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
	def setUp(self):
		# Setting up a fake user logged-in
		u = User(username='test')
		u.set_password('0000')
		u.save()
		self.main_client = Client()
		self.main_client.login(username='test', password='0000')

	def test_AccessNonExistentModel(self):
		model = RandomGenerator.genRandomString(especific_long=100)
		response =  self.main_client.get('/admins/modelos/'+model)
		self.assertEqual(response.status_code,404)

	def test_AccessNonExistentKey(self):
		'''
			Se selecciona usuario para el test porque ya en setUp se hace
			incersion de un usuario ficticio para la prueba
		'''
		key = RandomGenerator.genRandomInteger(min_value=10,max_value=100)
		response =  self.main_client.get('/admins/modelos/usuario/editar/'+str(key))
		self.assertEqual(response.status_code,404)		


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

	def test_inputEmptyName(self):
		model_object = TipoDocente(nombre = '')
		form = FormFactory.genForm('tipo docente',model_object)
		self.assertTrue(not form.is_valid())

	#Pruebas Backend
	def test_create(self):
		self.assertEqual(TipoDocente.objects.count(),0)
		response =  self.main_client.post('/admins/modelos/tipo docente/crear', {'nombre': 'abc'})
		self.assertEqual(response.status_code,200)
		self.assertEqual(TipoDocente.objects.count(),1)

	def test_delete(self):
		self.assertEqual(TipoDocente.objects.count(),0)		
		l = len(TipoDocente.objects.all())
		temp = TipoDocente(nombre='abc')
		temp.save()
		self.assertEqual(TipoDocente.objects.count(),1)
		response = self.main_client.post('/admins/modelos/tipo docente/borrar/'+str(temp.pk))
		self.assertEqual(response.status_code,200)
		self.assertEqual(TipoDocente.objects.count(),0)

	def test_update(self):
		self.assertEqual(TipoDocente.objects.count(),0)	
		temp = TipoDocente.objects.create(nombre='abc')
		self.assertEqual(TipoDocente.objects.count(),1)	
		pkey = temp.pk
		old = temp.nombre
		response = self.main_client.post('/admins/modelos/tipo docente/editar/'+str(temp.pk),{'nombre':'cba'})
		temp = TipoDocente.objects.get(pk=pkey)
		self.assertEqual(response.status_code,200)
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
		self.assertEqual(JerarquiaDocente.objects.count(),0)
		response =  self.main_client.post('/admins/modelos/jerarquia docente/crear', {'jerarquia':1, 'nombre': 'abc','tipo_docente':1})
		self.assertEqual(response.status_code,200)
		self.assertEqual(JerarquiaDocente.objects.count(),1)

	def test_delete(self):
		self.assertEqual(JerarquiaDocente.objects.count(),0)		
		model_object = JerarquiaDocente.objects.create(
			jerarquia = 6,
			nombre=  'abc',
			tipo_docente_id = 1)
		self.assertEqual(JerarquiaDocente.objects.count(),1)
		response = self.main_client.post('/admins/modelos/jerarquia docente/borrar/'+str(model_object.pk))
		self.assertEqual(response.status_code,200)
		self.assertEqual(JerarquiaDocente.objects.count(),0)

	def test_update(self):
		self.assertEqual(JerarquiaDocente.objects.count(),0)	
		model_object = JerarquiaDocente.objects.create(
			jerarquia = 6,
			nombre=  'abc',
			tipo_docente_id = 1)
		self.assertEqual(JerarquiaDocente.objects.count(),1)
		pkey = model_object.pk
		old = (model_object.nombre,model_object.jerarquia,model_object.tipo_docente)
		response = self.main_client.post('/admins/modelos/jerarquia docente/editar/'+str(model_object.pk),{'jerarquia':1,'nombre':'cba','tipo_docente':1})
		temp = JerarquiaDocente.objects.get(pk=pkey)
		self.assertEqual(response.status_code,200)
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
	def test_insertExistentUser(self):
		self.assertEqual(Usuario.objects.count(),0)
		response =  self.main_client.post('/admins/modelos/usuario/crear', 
		{'usuario_id' :'123456','nombre' : 'test','apellido' : 'test', 'password' : '1234',
		'correo_Electronico' : 'example@domain.com' ,'telefono_celular' : '123456',
		'telefono_oficina' : '123456','telefono_casa' : '12356','fecha_ingreso' : '1/1/2013',	'direccion' : '',
		'dedicacion' : '6 hrs','estatus' : 'A',	'jerarquia_docente' : 1, 'tipo_contrato' : 1,'centro' : 1})	
		self.assertEqual(response.status_code,200)
		self.assertEqual(Usuario.objects.count(),0)

	def test_createUniqueUser(self):
		self.assertEqual(Usuario.objects.count(),0)
		response =  self.main_client.post('/admins/modelos/usuario/crear', 
		{'usuario_id' :'123457','nombre' : 'test','apellido' : 'test', 'password' : '1234',
		'correo_Electronico' : 'example@domain.com' ,'telefono_celular' : '123456',
		'telefono_oficina' : '123456','telefono_casa' : '12356','fecha_ingreso' : '1/1/2013',	'direccion' : '',
		'dedicacion' : '6 hrs','estatus' : 'A',	'jerarquia_docente' : 1, 'tipo_contrato' : 1,'centro' : 1})
		self.assertEqual(response.status_code,200)
		self.assertEqual(Usuario.objects.count(),1)

	def test_delete(self):
		u =Usuario.objects.create(usuario_id_id=1, telefono_celular = '123456',
		telefono_oficina = '123456',telefono_casa = '12356',fecha_ingreso = '2013-1-1',	direccion ='' ,
		dedicacion = '6 hrs',estatus = 'A',	jerarquia_docente_id = 1, tipo_contrato_id = 1,centro_id = 1)
		self.assertEqual(Usuario.objects.count(),1)
		response =  self.main_client.post('/admins/modelos/usuario/borrar/'+str(u.pk)) 
		self.assertEqual(response.status_code,200)
		self.assertEqual(Usuario.objects.count(),0)

	def test_update(self):
		u =Usuario.objects.create(usuario_id_id=1, telefono_celular = '123456',
		telefono_oficina = '12345',telefono_casa = '12356',fecha_ingreso = '2013-1-1',	direccion ='' ,
		dedicacion = '6 hrs',estatus = 'A',	jerarquia_docente_id = 1, tipo_contrato_id = 1,centro_id = 1)
		self.assertEqual(Usuario.objects.count(),1)
		name = u.usuario_id.first_name 
		pkey = u.pk
		response =  self.main_client.post('/admins/modelos/usuario/editar/'+str(u.pk), 
		{'usuario_id' :'123456','nombre' : 'NEW NAME','apellido' : 'test', 'password' : '1234',
		'correo_Electronico' : 'example@domain.com' ,'telefono_celular' : '123456',
		'telefono_oficina' : '123456','telefono_casa' : '12356','fecha_ingreso' : '1/1/2013',	'direccion' : '',
		'dedicacion' : '6 hrs','estatus' : 'A',	'jerarquia_docente' : 1, 'tipo_contrato' : 1,'centro' : 1})
		self.assertEqual(response.status_code,200)
		new_name = Usuario.objects.get(pk=pkey).usuario_id.first_name
		self.assertTrue(name != new_name)

"""
	codigo = models.PositiveIntegerField(unique=True)
	nombre = models.CharField(max_length=100L, unique=True)
	tipo_materia = models.CharField( max_length= 20, choices = (('Obligatoria','Obligatoria'),('Electiva','Electiva'), ('Electiva Obligatoria','Electiva Obligatoria'), ('Complementaria', 'Complementaria'), ('Laboratorio','Laboratorio')))
	unidades_credito_teoria = models.PositiveIntegerField()
	unidades_credito_practica = models.PositiveIntegerField()
	unidades_credito_laboratorio = models.PositiveIntegerField()
	estatus = models.CharField(max_length= 1, choices = (('A','Activa'), ('I','Inactiva')))
	semestre = models.PositiveIntegerField(blank=True,null=True)
	centro = models.ForeignKey(Centro)
"""
class MateriaTest(TestCase):
	def setUp(self):
		# Setting up a fake user logged-in
		self.u = User(pk=1,username='test')
		self.u.set_password('0000')
		self.u.save()
		self.main_client = Client()
		self.main_client.login(username='test', password='0000')
		self.Centro = Centro.objects.create(pk=1,nombre='xcentro', area='any')
		self.model_object = Materia(codigo=6602,
		nombre = 'xnombre', tipo_materia = 'Laboratorio',
		unidades_credito_teoria =2 ,unidades_credito_practica = 2,
		unidades_credito_laboratorio =2 , estatus = 'A',
		semestre = 2013, centro_id = 1)

	def test_invalidCodigo(self):
		self.model_object.codigo = RandomGenerator.genRandomInteger(valid=False)
		form = FormFactory.genForm('materia', self.model_object)
		self.assertEqual(form.is_valid(),False)

	def test_tolongName(self):
		self.model_object.nombre = RandomGenerator.genRandomString(especific_long=150)
		form = FormFactory.genForm('materia', self.model_object)
		self.assertEqual(form.is_valid(),False)

	def test_invalidTipoMateria(self):
		self.model_object.tipo_materia = '(:'
		form = FormFactory.genForm('materia', self.model_object)
		self.assertEqual(form.is_valid(),False)
	
	def test_invalidUnidades(self):
		self.model_object.unidades_credito_teoria =-1
		form = FormFactory.genForm('materia', self.model_object)
		self.assertEqual(form.is_valid(),False)

		self.model_object.unidades_credito_teoria = 1
		self.model_object.unidades_credito_practica = -1
		form = FormFactory.genForm('materia', self.model_object)
		self.assertEqual(form.is_valid(),False)

		self.model_object.unidades_credito_practica = 1
		self.model_object.unidades_credito_laboratorio = -1		
		form = FormFactory.genForm('materia', self.model_object)
		self.assertEqual(form.is_valid(),False)

	def test_invalidEstatus(self):
		self.model_object.estatus =  'INVALID',
		form = FormFactory.genForm('materia', self.model_object)
		self.assertEqual(form.is_valid(),False)

	def test_invalidSemestre(self):
		self.model_object.semestre = -2000
		form = FormFactory.genForm('materia', self.model_object)
		self.assertEqual(form.is_valid(),False)

	#Pruebas Bckend:
	def test_create(self):
		self.assertEqual(Materia.objects.count(),0)
		response =  self.main_client.post('/admins/modelos/materia/crear', 
		{'codigo':'6603',
		'nombre' : 'xnombre', 'tipo_materia' : 'Laboratorio',
		'unidades_credito_teoria' : '2' ,'unidades_credito_practica' : '2',
		'unidades_credito_laboratorio' :'2' , 'estatus' : 'A',
		'semestre' : '6', 'centro': 1})
		self.assertEqual(response.status_code,200)
		self.assertEqual(Materia.objects.count(),1)

	def test_delete(self):
		m = Materia.objects.create(codigo=6602,	nombre = 'xnombre', tipo_materia = 'Laboratorio',
		unidades_credito_teoria =2 ,unidades_credito_practica = 2,
		unidades_credito_laboratorio =2 , estatus = 'A',semestre = 2013, centro_id = 1)
		self.assertEqual(Materia.objects.count(),1)
		response =  self.main_client.post('/admins/modelos/materia/borrar/'+str(m.pk)) 
		self.assertEqual(response.status_code,200)
		self.assertEqual(Materia.objects.count(),0)

	def test_update(self):
		m = Materia.objects.create(codigo=6602,	nombre = 'xnombre', tipo_materia = 'Laboratorio',
		unidades_credito_teoria =2 ,unidades_credito_practica = 2,
		unidades_credito_laboratorio =2 , estatus = 'A',semestre = 2013, centro_id = 1)
		self.assertEqual(Materia.objects.count(),1)
		name = m.nombre 
		pkey = m.pk
		response =  self.main_client.post('/admins/modelos/materia/editar/'+str(m.pk), 
		{'codigo':6602,	'nombre' : 'NEW NAME', 'tipo_materia' : 'Laboratorio',
		'unidades_credito_teoria' :2 ,'unidades_credito_practica' : 2,
		'unidades_credito_laboratorio' :2 , 'estatus' : 'A','semestre' : 2013, 'centro' : 1})
		self.assertEqual(response.status_code,200)
		new_name = Materia.objects.get(pk=pkey).nombre
		self.assertTrue(name != new_name)

#----------------------- Pruebas unitarias CRUD Aula ----------------------#

class AulaTestCases(TestCase):

    def setUp(self):
        self.a = Aula(aula_id=1,tipo_aula='I',capacidad=30,estatus_aula='A')
        self.a2 = Aula(aula_id=10,tipo_aula='E',capacidad=20,estatus_aula='A')
        self.a.save()
        self.a2.save()
        self.u = User.objects.create_user(username='brucewayne', email='batman@gmail.com', password='batman')
        self.f = RequestFactory()

    def test_InsertarAula(self):
        self.client.login(username='brucewayne',password='batman')

        #Es el modelo correcto
        response = self.client.post("/admins/modelos/aula/crear")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['modelo'],'aula')

        #Campos vacios
        response = self.client.post('/admins/modelos/aula/crear', {'tipo_aula':'E','capacidad':20,'estatus_aula':'A'})
        self.assertEqual(response.context['form']['aula_id'].errors, [u'Este campo es obligatorio.'])

        response = self.client.post('/admins/modelos/aula/crear', {'aula_id':2,'capacidad':20,'estatus_aula':'A'})
        self.assertEqual(response.context['form']['tipo_aula'].errors, [u'Este campo es obligatorio.'])

        response = self.client.post('/admins/modelos/aula/crear', {'aula_id':2,'tipo_aula':'E','estatus_aula':'A'})
        self.assertEqual(response.context['form']['capacidad'].errors, [u'Este campo es obligatorio.'])

        response = self.client.post('/admins/modelos/aula/crear', {'aula_id':2,'tipo_aula':'E','capacidad':20})
        self.assertEqual(response.context['form']['estatus_aula'].errors, [u'Este campo es obligatorio.'])

        #Insercion correcta
        response = self.client.post('/admins/modelos/aula/crear', {'aula_id':2,'tipo_aula':'E','capacidad':20,'estatus_aula':'A'})
        self.assertRedirects(response,"/admins/modelos/aula",302,200)

        #Insercion con id repetido
        response = self.client.post('/admins/modelos/aula/crear', {'aula_id':2,'tipo_aula':'I','capacidad':10,'estatus_aula':'I'})
        self.assertEqual(response.context['form']['aula_id'].errors, [u'Ya existe Aula con este Aula id.'])

        #Insercion con campos incorrectos
        response = self.client.post('/admins/modelos/aula/crear', {'aula_id':4,'tipo_aula':'Z','capacidad':10,'estatus_aula':'A'})
        self.assertEqual(response.context['form']['tipo_aula'].errors, [u'Escoja una opci\xf3n v\xe1lida. Z no es una de las opciones disponibles.'])

        response = self.client.post('/admins/modelos/aula/crear', {'aula_id':4,'tipo_aula':'L','capacidad':'Z','estatus_aula':'A'})
        self.assertEqual(response.context['form']['capacidad'].errors, [u'Introduzca un n\xfamero completo.'])

        response = self.client.post('/admins/modelos/aula/crear', {'aula_id':4,'tipo_aula':'L','capacidad':10,'estatus_aula':'Z'})
        self.assertEqual(response.context['form']['estatus_aula'].errors, [u'Escoja una opci\xf3n v\xe1lida. Z no es una de las opciones disponibles.'])


        #Insercion con numeros grandes
        response = self.client.post('/admins/modelos/aula/crear', {'aula_id': RandomGenerator.genRandomInteger(valid=True,min_value=3,max_value=100000),'tipo_aula':'E','capacidad':20,'estatus_aula':'A'})
        self.assertRedirects(response,"/admins/modelos/aula",302,200)
        response = self.client.post('/admins/modelos/aula/crear', {'aula_id': 4,'tipo_aula':'E','capacidad':RandomGenerator.genRandomInteger(valid=True,min_value=3,max_value=100000),'estatus_aula':'A'})
        self.assertRedirects(response,"/admins/modelos/aula",302,200)
        response = self.client.post('/admins/modelos/aula/crear', {'aula_id': RandomGenerator.genRandomInteger(valid=True,min_value=3,max_value=100000),'tipo_aula':'E','capacidad':RandomGenerator.genRandomInteger(valid=True,min_value=3,max_value=100000),'estatus_aula':'A'})
        self.assertRedirects(response,"/admins/modelos/aula",302,200)

        #Deben existir 5 registros
        self.assertEqual(Aula.objects.count(),6)

    def test_EditarAula(self):
        self.client.login(username='brucewayne',password='batman')

        aula = Aula.objects.filter().all()[0]

        #Es el modelo correcto
        response = self.client.post("/admins/modelos/aula/editar/"+str(aula.pk))
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['modelo'],'aula')

        #Campos vacios
        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'tipo_aula':aula.tipo_aula,'capacidad':aula.capacidad,'estatus_aula':aula.estatus_aula})
        self.assertEqual(response.context['form']['aula_id'].errors, [u'Este campo es obligatorio.'])

        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'aula_id':aula.aula_id,'capacidad':aula.capacidad,'estatus_aula':aula.estatus_aula})
        self.assertEqual(response.context['form']['tipo_aula'].errors, [u'Este campo es obligatorio.'])

        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'aula_id':aula.aula_id,'tipo_aula':aula.tipo_aula,'estatus_aula':aula.estatus_aula})
        self.assertEqual(response.context['form']['capacidad'].errors, [u'Este campo es obligatorio.'])

        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'aula_id':aula.id,'tipo_aula':aula.tipo_aula,'capacidad':aula.capacidad})
        self.assertEqual(response.context['form']['estatus_aula'].errors, [u'Este campo es obligatorio.'])

        #Edicion correcta
        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'aula_id':str(aula.aula_id),'tipo_aula':aula.tipo_aula,'capacidad':aula.capacidad,'estatus_aula':aula.estatus_aula})
        self.assertRedirects(response,"/admins/modelos/aula",302,200)

        #Edicion con id repetido
        aula2 =  Aula.objects.filter().all()[1]
        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'aula_id':aula2.aula_id,'tipo_aula':aula.tipo_aula,'capacidad':aula.capacidad,'estatus_aula':aula.estatus_aula})
        self.assertEqual(response.context['form']['aula_id'].errors, [u'Ya existe Aula con este Aula id.'])

        #Edicion con campos incorrectos
        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'aula_id':aula.aula_id,'tipo_aula':'Z','capacidad':aula.capacidad,'estatus_aula':aula.estatus_aula})
        self.assertEqual(response.context['form']['tipo_aula'].errors, [u'Escoja una opci\xf3n v\xe1lida. Z no es una de las opciones disponibles.'])

        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'aula_id':aula.aula_id,'tipo_aula':aula.tipo_aula,'capacidad':aula.capacidad,'estatus_aula':'Z'})
        self.assertEqual(response.context['form']['estatus_aula'].errors, [u'Escoja una opci\xf3n v\xe1lida. Z no es una de las opciones disponibles.'])

        #Edicion con numeros grandes
        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'aula_id': RandomGenerator.genRandomInteger(valid=True,min_value=3,max_value=100000),'tipo_aula':aula.tipo_aula,'capacidad':aula.capacidad,'estatus_aula':aula.estatus_aula})
        self.assertRedirects(response,"/admins/modelos/aula",302,200)
        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'aula_id':aula.aula_id,'tipo_aula':aula.tipo_aula,'capacidad':RandomGenerator.genRandomInteger(valid=True,min_value=3,max_value=100000),'estatus_aula':aula.estatus_aula})
        self.assertRedirects(response,"/admins/modelos/aula",302,200)
        response = self.client.post('/admins/modelos/aula/editar/'+str(aula.pk), {'aula_id': RandomGenerator.genRandomInteger(valid=True,min_value=3,max_value=100000),'tipo_aula':aula.tipo_aula,'capacidad':RandomGenerator.genRandomInteger(valid=True,min_value=3,max_value=100000),'estatus_aula':aula.estatus_aula})
        self.assertRedirects(response,"/admins/modelos/aula",302,200)

        #Deben existir 5 registros
        self.assertEqual(Aula.objects.count(),2)

    def test_BorrarAula(self):
        remaining = Aula.objects.count()-1
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula/borrar/"+str(self.a.pk))
        self.assertRedirects(response,"/admins/modelos/aula",302,200)
        self.assertEqual(Aula.objects.count(),remaining)

    def test_ListarAula(self):
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['modelo'],'aula')

    def test_LeerAula(self):
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula/"+str(self.a.pk))
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['modelo'],'aula')

    def test_LeerAulaNoExiste(self):
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula/100000")
        self.assertEqual(response.status_code,404)

    def test_BorrarAulaNoExiste(self):
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula/borrar/100000")
        self.assertEqual(response.status_code,404)

    def test_EditarAulaNoExiste(self):
        self.client.login(username='brucewayne',password='batman')
        response = self.client.post("/admins/modelos/aula/editar/100000")
        self.assertEqual(response.status_code,404)

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

#------------------------ Pruebas unitarias CRUD Aula -----------------------#
