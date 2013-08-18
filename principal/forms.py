#encoding:utf-8
from django import forms
from principal.models import *
from django.db.models.loading import get_app, get_models, get_model
from django.contrib.contenttypes.models import ContentType 


class LoginForm(forms.Form):
	user = forms.IntegerField(error_messages={'required': 'Campo Obligatorio','invalid': 'Este campo debe ser númerico'}, min_value = 1, label = "Usuario")
	password = forms.CharField(error_messages={'required': 'Campo Obligatorio'}, widget=forms.PasswordInput(), label = 'Contraseña')


def get_object_form( type_id,  excludes=None):
	ctype = ContentType.objects.get( pk=type_id ) 
	model_class = ctype.model_class( ) 
	class _ObjectForm( forms.ModelForm ):
		class Meta:
			model = model_class
			#excludes = excludes
	return _ObjectForm
	



	

