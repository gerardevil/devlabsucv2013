#encoding:utf-8
#forms.py

from django import forms
from principal.models import *
from django.contrib.auth.hashers import *
from django.contrib.contenttypes.models import ContentType 
from django.db.models.loading import get_app, get_models, get_model
from principal.manager.formValidators import validateUniqueUser,validateIntegerField,validateExistUser

class LoginForm(forms.Form):
	user = forms.IntegerField(error_messages={'required': 'Campo Obligatorio','invalid': 'Este campo debe ser númerico'}, min_value = 1, label = "Usuario")
	password = forms.CharField(error_messages={'required': 'Campo Obligatorio'}, widget=forms.PasswordInput(), label = 'Contraseña')

class CustomUserForm(forms.Form):
	# Fields for User Django model
	usuario_id = forms.IntegerField(error_messages={'required': 'Campo Obligatorio','invalid': 'Este campo debe ser númerico'}, validators = [validateUniqueUser,validateIntegerField], min_value = 1, label = "Cedula")
	nombre = forms.CharField(error_messages={'required': 'Campo Obligatorio'})
	apellido = forms.CharField(error_messages={'required': 'Campo Obligatorio'})
	password = forms.CharField(error_messages={'required': 'Campo Obligatorio'}, widget=forms.PasswordInput(render_value = True), label = 'Contraseña')
	correo_Electronico = forms.EmailField(error_messages={'required': 'Campo Obligatorio','invalid': 'Formato de correo aceptado usuario@dominio.com'}) 
	
	# Fields for Devlabs Team User model
	telefono_celular = forms.CharField(error_messages={'required': 'Campo Obligatorio'},max_length=20L,label='Telefono Celular')
	telefono_oficina = forms.CharField(error_messages={'required': 'Campo Obligatorio'},max_length=20L,label='Telefono Oficina')
	telefono_casa = forms.CharField(required=False, max_length=20L,label = 'Telefono Casa')	
	fecha_ingreso = forms.DateField(error_messages={'required': 'Campo Obligatorio','invalid':'Formato de Fecha aceptado: Dia/Mes/Año'},input_formats = ['%Y-%m-%d'])	
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
    #aula = forms.ModelChoiceField(required=True,error_messages={'required': 'Campo Obligatorio'}, queryset=Aula.objects)
    materia = forms.ModelChoiceField(required=True,error_messages={'required': 'Campo Obligatorio'}, queryset=MateriaOfertada.objects.filter(materia__in=Materia.objects.filter(tipo_materia='Obligatoria')))


class AgregarMateriaEForm(forms.Form):
    materia = forms.ModelChoiceField(required=True,error_messages={'required': 'Campo Obligatorio'}, queryset=MateriaOfertada.objects.filter(materia__in=Materia.objects.filter(tipo_materia='Electiva' or 'Complementaria')))
    dia_semana = forms.ChoiceField(required=True,error_messages={'required': 'Campo Obligatorio'},choices= (('Lunes','Lunes'), ('Martes','Martes'), ('Miercoles','Miercoles'), ('Jueves','Jueves'), ('Viernes','Viernes') ))
    hora_inicio = forms.TimeField(required=True,error_messages={'required': 'Campo Obligatorio'})
    hora_fin = forms.TimeField(required=True,error_messages={'required': 'Campo Obligatorio'})
    aula = forms.ModelChoiceField(required=True,error_messages={'required': 'Campo Obligatorio'}, queryset=Aula.objects)

    def __init__(self, *args, **kwargs):
        self.ukey = kwargs.pop('ukey')
        super(AgregarMateriaEForm, self).__init__(*args, **kwargs)

    def save(self):
        u = Usuario.objects.get(pk=self.ukey)
        cse = MateriaSolicitada.objects.filter(estatus='N',usuario=u,materia=self.cleaned_data['materia']).count()
        if (cse == 0):
            ms = MateriaSolicitada(estatus='N',usuario=u,materia=self.cleaned_data['materia'])
            ms.save()
        else:
            ms = MateriaSolicitada.objects.get(usuario=u,materia=self.cleaned_data['materia'])

        HorarioSolicitado.objects.create(
        dia_semana=self.cleaned_data['dia_semana'],
        hora_inicio=self.cleaned_data['hora_inicio'],
        hora_fin=self.cleaned_data['hora_fin'],
        horario_solicitado=ms,
        aula=self.cleaned_data['aula'])

class EditarMateriaE(forms.Form):
    dia_semana = forms.ChoiceField(required=True,error_messages={'required': 'Campo Obligatorio'},choices = (('Lunes','Lunes'), ('Martes','Martes'), ('Miercoles','Miercoles'), ('Jueves','Jueves'), ('Viernes','Viernes') ))
    hora_inicio = forms.TimeField(required=True,error_messages={'required': 'Campo Obligatorio'})
    hora_fin = forms.TimeField(required=True,error_messages={'required': 'Campo Obligatorio'})
    aula = forms.ModelChoiceField(required=True,error_messages={'required': 'Campo Obligatorio'},queryset=Aula.objects.all())

    def __init__(self, *args, **kwargs):
        self.hkey = kwargs.pop('hkey')
        hs = HorarioSolicitado.objects.get(pk=self.hkey)
        super(EditarMateriaE, self).__init__(*args, **kwargs)
        self.fields['dia_semana'].initial=hs.dia_semana
        self.fields['hora_inicio'].initial=hs.hora_inicio
        self.fields['hora_fin'].initial=hs.hora_fin
        self.fields['aula'].initial=hs.aula

    def save(self):
        #datos = self.cleaned_data
        hs = HorarioSolicitado.objects.get(pk=self.hkey)
        hs.dia_semana=self.cleaned_data['dia_semana']
        hs.hora_inicio=self.cleaned_data['hora_inicio']
        hs.hora_fin=self.cleaned_data['hora_fin']
        hs.aula = self.cleaned_data['aula']
        hs.save()


class EditarMateriaO(forms.Form):

    horario = forms.ModelChoiceField(required=True,error_messages={'required': 'Campo Obligatorio'},queryset=HorarioMateria.objects.all())
    #aula = forms.ModelChoiceField(required=True,error_messages={'required': 'Campo Obligatorio'},queryset=Aula.objects.all())

    def __init__(self, *args, **kwargs):
        self.hkey = kwargs.pop('hkey')
        self.ukey = kwargs.pop('ukey')
        x = kwargs.pop('mat')
        self.m = Materia.objects.all()[:1]
        hs = HorarioSolicitado.objects.get(pk=self.hkey)
        super(EditarMateriaO, self).__init__(*args, **kwargs)
        self.fields['horario'] = forms.ModelChoiceField(queryset=HorarioMateria.objects.filter(materia=x))
        #self.fields['aula'].initial=hs.aula

    def save(self):
        #datos = self.cleaned_data
        hs = HorarioSolicitado.objects.get(pk=self.hkey)
        h = self.cleaned_data['horario']
        hs.dia_semana= h.dia_semana
        hs.hora_inicio = h.hora_inicio
        hs.hora_fin = h.hora_fin
        #hs.aula = self.cleaned_data['aula']
        hs.save()

class ResetPasswordRequestForm(forms.Form):
	username = forms.IntegerField(error_messages={'required': 'Campo Obligatorio','invalid': 'Este campo debe ser númerico'}, validators = [validateIntegerField,validateExistUser], min_value = 1, label = "Cédula")

class ResetPasswordChangeForm(forms.Form):
	password = forms.CharField(error_messages={'required':'Campo Obligatorio'}, widget=forms.PasswordInput(render_value = True), label = 'Nueva Contraseña')
	password_confirm = forms.CharField(error_messages={'required':'Campo Obligatorio'}, widget=forms.PasswordInput(render_value = True), label = 'Confirmar Contraseña')


class CambiarContrasena(forms.Form):
	contrasenaVieja = forms.CharField(error_messages={'required':'Campo Obligatorio'}, widget=forms.PasswordInput(render_value = True), label = 'Contraseña actual')
	contrasenaNueva = forms.CharField(error_messages={'required':'Campo Obligatorio'}, widget=forms.PasswordInput(render_value = True), label = 'Contraseña nueva')
	confirmarContrasena = forms.CharField(error_messages={'required':'Campo Obligatorio'}, widget=forms.PasswordInput(render_value = True), label = 'Confirmar contraseña')



def get_object_form( type_id ):
	ctype = ContentType.objects.get( pk=type_id ) 
	model_class = ctype.model_class() 
	class _ObjectForm( forms.ModelForm ):
		class Meta:
			model = model_class
	return _ObjectForm
