from django.test import TestCase
from datetime import datetime
from random import *
import sys

# Generadores aleatorios para pruebas unitarias #
#################################################

class RandomGenerator(object):
	
	def __init__(self):
		seed()
		self.ascii_set = map ((lambda i : chr(i)),range(33,127))
		self.extended_ascii_set = map ((lambda i : chr(i)),range(33,240))
		self.maxInt = sys.maxint
		self.minInt = -sys.maxint
		self.maxyear =  datetime.now().year + 1000
		self.maxEmailLen =  254  # Acording with RFC3696/532
		self.validEmailset = ['niceandsimple@example.com','very.common@example.com','a.little.lengthy.but.fine@dept.example.com', 'disposable.style.email.with+symbol@example.com', '"very.unusual.@.unusual.com"@example.com']
		self.invalidEmailset =  ['Abc.example.com','A@b@c@example.com' ,'a"b(c)d,e:f;g<h>i[j\k]l@example.com','just"not"right@example.com','this is"not\\allowed@example.com','this\ still\"not\\allowed@example.com']
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
	def genRandomString(self,weird = False, especific_long = None, max_long = 1000):
		string = ''
		l = (len(self.ascii_set) if not weird else len(self.extended_ascii_set))-1
		set = self.ascii_set if not weird else self.extended_ascii_set
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
	def genRandomDate(self,valid=True, separator=None):

		date = ''
		if separator or len(separator)!= 1:			
			if valid :
				year = randint(1958, datetime.now().year)
				month = randint(1, 12)
				day = randint(1, 31) if month in [1,5,7,8,10,12] else (randint(1, 30) if month != 2 else 28)
			else:
				year = randint(0,self.maxyear)
				month = randint(0, 70)
				day = randint(0, 70)
			date = str(day)+separator+str(month)+separator+str(year)
		return date

	'''
		-genRandomTime-
		valid (opcional): valid = True , sugiere generacion
		de horas validas, en formato de 24 horas.
	'''
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
	def genEmail(self,valid=True, empty = False):
		email = ''
		if not empty:
			if valid :
				email = self.validEmailset[randint(0,len(self.validEmailset)-1)]			
			else:
				if randint(0,1) == 0:
					email = self.invalidEmailset[randint(0,len(self.invalidEmailset)-1)]
				else:
					email = ('a'*self.maxEmailLen)+'@domain.com'
		return email

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 5)
