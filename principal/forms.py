from django import forms
from principal.models import Usuario


class UsuarioForm(forms.ModelForm):
	class Meta:
		model = Usuario