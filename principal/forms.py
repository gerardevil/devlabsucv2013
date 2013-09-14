#encoding:utf-8
#forms.py

from django import forms
from principal.models import *
from principal.manager.formValidators import validateUniqueUser
from django.db.models.loading import get_app, get_models, get_model
from django.contrib.contenttypes.models import ContentType 
from django.contrib.auth.hashers import *


class LoginForm(forms.Form):
	user = forms.IntegerField(error_messages={'required': 'Campo Obligatorio','invalid': 'Este campo debe ser númerico'}, min_value = 1, label = "Usuario")
	password = forms.CharField(error_messages={'required': 'Campo Obligatorio'}, widget=forms.PasswordInput(), label = 'Contraseña')

class CustomUserForm(forms.Form):
	# Fields for User Django model
	usuario_id = forms.IntegerField(error_messages={'required': 'Campo Obligatorio','invalid': 'Este campo debe ser númerico'}, validators = [validateUniqueUser], min_value = 1, label = "Cedula")
	nombre = forms.CharField(error_messages={'required': 'Campo Obligatorio'})
	apellido = forms.CharField(error_messages={'required': 'Campo Obligatorio'})
	password = forms.CharField(error_messages={'required': 'Campo Obligatorio'}, widget=forms.PasswordInput(render_value = True), label = 'Contraseña')
	correo_Electronico = forms.EmailField(error_messages={'required': 'Campo Obligatorio','invalid': 'Formato de correo aceptado usuario@dominio.com'}) 
	
	# Fields for Devlabs Team User model
	telefono_celular = forms.CharField(error_messages={'required': 'Campo Obligatorio'},max_length=20L,label='Telefono Celular')
	telefono_oficina = forms.CharField(error_messages={'required': 'Campo Obligatorio'},max_length=20L,label='Telefono Oficina')
	telefono_casa = forms.CharField(required=False, max_length=20L,label = 'Telefono Casa')	
	fecha_ingreso = forms.DateField(error_messages={'required': 'Campo Obligatorio','invalid':'Formato de Fecha aceptado: Dia/Mes/Año'},input_formats = ['%d/%m/%Y'])	
	direccion = forms.CharField(required=False,max_length=500L)
	dedicacion = forms.ChoiceField(error_messages={'required': 'Campo Obligatorio'}, choices = (('6 hrs','6 Horas'), ('8 hrs','8 Horas'), ('12 hrs','12 Horas'), ('20 hrs','20 Horas'), ('40 hrs','40 Horas'),('DE','Dedicacion Exclusiva')))
	estatus = forms.ChoiceField(error_messages={'required': 'Campo Obligatorio'}, choices=[('A','Activo'),('I','Inactivo'),('ED','Emergencia Docente')])
	jerarquia_docente = forms.ModelChoiceField(error_messages={'required': 'Campo Obligatorio'}, queryset=JerarquiaDocente.objects.all())
	tipo_contrato = forms.ModelChoiceField(error_messages={'required': 'Campo Obligatorio'}, queryset=TipoContrato.objects.all())
	centro = forms.ModelChoiceField(error_messages={'required': 'Campo Obligatorio'}, queryset=Centro.objects.all())
	
	def __init__(self, hide, *args, **kwargs):
		super(CustomUserForm,self).__init__(*args,**kwargs)
		if not hide:
			self.fields['usuario_id'] = forms.IntegerField(error_messages={'required': 'Campo Obligatorio','invalid': 'Este campo debe ser númerico'}, min_value = 1, label = "Cedula")
	
	def save(self,pastPk=None):
		data = self.cleaned_data
		# Divide cases between update and purely save.
		try:
			user = User.objects.get(username=str(pastPk))
		except Exception, e:
			user = User(username=data['usuario_id'], first_name=data['nombre'], last_name=data['apellido'],email=data['correo_Electronico'])
			user.set_password(data['password'])# hashing into sha256 
		else:
			user.username = str(data['usuario_id'])			
			user.email= data['correo_Electronico']
			user.first_name= data['nombre']
			user.last_name= data['apellido']
			if is_password_usable(data['password']):
				user.password = data['password']
			else:
				user.set_password(data['password'])# hashing into sha256 
		
		user.save()
		
		try:
		 	userProfile = Usuario.objects.get(usuario_id=user.pk)
		except Exception, e:
		 	userProfile = Usuario(usuario_id = user, telefono_celular = data['telefono_celular'], telefono_oficina  = data['telefono_oficina'], telefono_casa  = data['telefono_casa'], fecha_ingreso = data['fecha_ingreso'], direccion = data['direccion'], dedicacion = data['dedicacion'], estatus = data['estatus'], jerarquia_docente = data['jerarquia_docente'], tipo_contrato = data['tipo_contrato'], centro = data['centro'])
		else:
			userProfile.usuario_id =user
			userProfile.telefono_celular = data['telefono_celular']
			userProfile.telefono_oficina  = data['telefono_oficina']
			userProfile.telefono_casa  = data['telefono_casa']
			userProfile.fecha_ingreso = data['fecha_ingreso']
			userProfile.direccion = data['direccion']
			userProfile.dedicacion = data['dedicacion']
			userProfile.estatus = data['estatus']
			userProfile.jerarquia_docente = data['jerarquia_docente']
			userProfile.tipo_contrato = data['tipo_contrato']
			userProfile.centro = data['centro']
		
		userProfile.save()


class AgregarMateriaForm(forms.Form):
    aula = forms.ModelChoiceField(error_messages={'required': 'Campo Obligatorio'}, queryset=Aula.objects)
    materia = forms.ModelChoiceField(error_messages={'required': 'Campo Obligatorio'}, queryset=MateriaOfertada.objects)






def get_object_form( type_id ):
	ctype = ContentType.objects.get( pk=type_id ) 
	model_class = ctype.model_class() 
	class _ObjectForm( forms.ModelForm ):
		class Meta:
			model = model_class
	return _ObjectForm
