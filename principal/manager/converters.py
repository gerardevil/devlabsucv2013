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