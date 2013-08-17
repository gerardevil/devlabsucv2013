#encoding:utf-8
from django import forms
from principal.models import *


class LoginForm(forms.Form):
	user = forms.IntegerField(min_value = 1, label = "Usuario")
	password = forms.CharField(widget=forms.PasswordInput(), label = 'Contraseña')

class UsuarioForm(forms.ModelForm):
	class Meta:
		model = Usuario

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula