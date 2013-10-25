#converters.py
import datetime

'''
	Official source : http://djangosnippets.org/snippets/2090/
'''

def convertDatetimeToString(o):
	DATE_FORMAT = "%d/%m/%Y" 
	TIME_FORMAT = "%H:%M:%S"

	if isinstance(o, datetime.date):
	    return o.strftime(DATE_FORMAT)
	elif isinstance(o, datetime.time):
	    return o.strftime(TIME_FORMAT)
	elif isinstance(o, datetime.datetime):
	    return o.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))

def translateStatus(status=''):
	description = "Non description found"

	if status == 'N' :
		description = "No enviado"
	elif status == 'P' :
		description = "Procesando"
	elif status == 'PJ' :
		description = "Procesando por Jefe de Departamento"
	elif status == 'AC' :
		description = "Aceptado por Coordinador de Centro"
	elif status == 'AJ' :
		description = "Aceptado por Jefe de Departamento"
	elif status == 'RC' :
		description = "Rechazado por Coordinador de Centro"
	elif status == 'RJ' :
		description = "Rechazado por Jefe de Departamento"

	return '<b>'+description+'</b>'
