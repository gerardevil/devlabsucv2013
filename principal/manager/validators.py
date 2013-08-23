from principal.models import *
from django.core.exceptions import ValidationError

##############################################
# All custom validator for from usage bellow #
##############################################

def validateUniqueUser(user_id):
    if User.objects.filter(username=str(user_id)).exists():
        raise ValidationError(u'El Usuario : %d , ya esta Registrado en el Sistema' % user_id)