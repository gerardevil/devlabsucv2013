#encoding:utf-8
#formsValidators.py

from principal.models import *
from django.core.exceptions import ValidationError

##############################################
# All custom validator for from usage bellow #
##############################################

def validateUniqueUser(user_id):
	if user_id:
	    if User.objects.filter(username=str(user_id)).exists():
	        raise ValidationError(u'El Usuario : %d , ya esta Registrado en el Sistema' % user_id)
	else:
		raise ValidationError('Este campo es obligatorio')

def validateIntegerField(user_id):
	if user_id :
		if not isinstance(int(user_id),int):
			raise ValidationError(u'Este Campo debe ser exclusivamente númerico')
	else:
		raise ValidationError('Este campo es obligatorio')

def validateExistUser(user_id):
	if user_id:
	   if not User.objects.filter(username=str(user_id)).exists():
	        raise ValidationError(u'%d no esta Registrado en el Sistema' % user_id)
	else:
		raise ValidationError('Este campo es obligatorio')
