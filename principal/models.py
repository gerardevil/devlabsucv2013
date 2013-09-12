#encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from principal.manager.converters import convertDatetimeToString

##########################################
# Models wich have no foreing key bellow #
##########################################


class Aula(models.Model):
	aula_id = models.CharField(max_length=10L,unique=True)
	tipo_aula = models.CharField(max_length=1L ,choices = (('I','Interna'), ('E','Externa'), ('L','Laboratorio')))
	capacidad = models.PositiveIntegerField()
	estatus_aula = models.CharField(max_length=1L, choices = (('A','Activa'), ('I','Inactiva')))

	class Meta:
		db_table = 'aula'

	def __unicode__(self):
		return u'aula: %s | tipo_aula: %s | capacidad: %d | estatus_aula: %s' % (self.aula_id, self.tipo_aula, self.capacidad, self.estatus_aula)

	def toJson(self,minify=True):
		retorno = {'aula_id':self.aula_id,
				'tipo_aula':self.tipo_aula,
				'capacidad':self.capacidad,
				'estatus_aula':self.estatus_aula
				}
		return retorno
	
	def toString(self):
		return self.tipo_aula + '      ' + self.aula_id

	def get_pk(self):
		return self.pk

class Centro(models.Model):
	nombre = models.CharField(max_length=100L,unique=True)
	area = models.CharField(max_length=100L)

	class Meta:
		db_table = 'centro'

	def __unicode__(self):
		return u'nombre: %s | area: %s' % (self.nombre, self.area)

	def toJson(self,minify=True):
		retorno = {
				'nombre':self.nombre,
				'area':self.area
				}
		return retorno
	
	def toString(self):
		return self.nombre

	def get_pk(self):
		return self.pk

class PeriodoAcademico(models.Model):
	periodo_lectivo = models.PositiveIntegerField()
	semestre = models.PositiveIntegerField()
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField()

	class Meta:
		db_table = 'periodo_academico'

	def __unicode__(self):
		return u'periodo_lectivo: %d | semestre: %d | inicio: %s | fin: %s' % (self.periodo_lectivo, self.semestre, convertDatetimeToString(self.fecha_inicio), convertDatetimeToString(self.fecha_fin))

	def toJson(self,minify=True):
		retorno = {'periodo_lectivo':self.periodo_lectivo,
				'semestre':self.semestre,
				'fecha_inicio':self.fecha_inicio,
				'fecha_fin':self.fecha_fin
				}
		return retorno

	def toString(self):
		return 'Semestre ' + str(self.semestre) + '-' + str(self.periodo_lectivo)
	
	def get_pk(self):
		return self.pk
		
class PropiedadesSistema(models.Model):
	propiedades_sistema_id = models.CharField(max_length=45, unique=True,blank=True)
	nombre = models.CharField(max_length=45)
	valor = models.CharField(max_length=45)

	class Meta:
		db_table = 'propiedades_sistema'

	def __unicode__(self):
		return u'System_prop_id: %s | nombre: %s | valor: %s' % (self.propiedades_sistema_id, self.nombre, self.valor)

	def toJson(self,minify=True):
		retorno = {'propiedades_sistema_id':self.propiedades_sistema_id,
				'nombre':self.nombre,
				'valor':self.valor
				}
		return retorno

	def toString(self):
		return self.nombre

	def get_pk(self):
		return self.pk
		
class Rol(models.Model):
	rol_id = models.CharField(max_length=20, unique=True)
	nombre = models.CharField(max_length=100, unique=True)
	descripcion = models.TextField(max_length=500, blank=True)

	class Meta:
		db_table = 'rol'

	def __unicode__(self):
		return u'rol_id: %s | nombre: %s | descripcion: %s' % (self.rol_id, self.nombre, self.descripcion)

	def toJson(self,minify=True):
		retorno = {'rol_id':self.rol_id,
				'nombre':self.nombre,
				'descripcion':self.descripcion
				}
		return retorno
		
	def toString(self):
		return self.nombre

	def get_pk(self):
		return self.pk

class TipoContrato(models.Model):
	nombre = models.CharField(max_length=45L, unique=True)

	class Meta:
		db_table = 'tipo_contrato'

	def __unicode__(self):
		return u'nombre: %s' % (self.nombre)

	def toJson(self,minify=True):
		retorno = {'nombre':self.nombre}
		return retorno
		
	def toString(self):
		return self.nombre

	def get_pk(self):
		return self.pk

class TipoDocente(models.Model):
	nombre = models.CharField(max_length=100L, unique=True)

	class Meta:
		db_table = 'tipo_docente'

	def __unicode__(self):
		return u'nombre: %s ' % (self.nombre)

	def toJson(self,minify=True):
		retorno = {'nombre':self.nombre	}
		return retorno
		
	def toString(self):
		return self.nombre

	def get_pk(self):
		return self.pk
		
				
##########################################
# Models wich do have foreing key bellow #
##########################################


class JerarquiaDocente(models.Model):
	jerarquia = models.PositiveIntegerField(unique=True)
	nombre = models.CharField(max_length=100, unique=True)
	tipo_docente = models.ForeignKey(TipoDocente)

	class Meta:
		db_table = 'jerarquia_docente'

	def __unicode__(self):
		return u'jerarquia: %d | nombre: %s | tipo_docente: %s' % (self.jerarquia,self.nombre, str(self.tipo_docente))

	def toJson(self,minify=True):
		retorno = {'jerarquia':self.jerarquia,'nombre':self.nombre,'tipo_docente':self.tipo_docente.pk}
		return retorno
		
	def toString(self):
		return self.nombre

	def get_pk(self):
		return self.pk

class Usuario(models.Model):
	
	''' 
	Using Django User model : Nombre, Apellido, Clave are on the  Django User model
	'''
	usuario_id = models.OneToOneField(User)
	telefono_celular = models.CharField(max_length=20L, blank=True)
	telefono_oficina = models.CharField(max_length=20L, blank=True)
	telefono_casa = models.CharField(max_length=20L, blank=True)
	fecha_ingreso = models.DateField(blank=True)
	direccion = models.TextField(max_length=1000L, blank=True)
	dedicacion = models.CharField(max_length=6) 
	estatus = models.CharField(max_length= 2)
	jerarquia_docente = models.ForeignKey(JerarquiaDocente)
	tipo_contrato = models.ForeignKey(TipoContrato)
	centro = models.ForeignKey(Centro)

	class Meta:
		db_table = 'usuario'

	def __unicode__(self):
		return u'usuario: %s | nombre: %s | apellido: %s | dedicacion: %s' % ( self.usuario_id.username, self.usuario_id.first_name, self.usuario_id.last_name, self.dedicacion)

	def toJson(self,minify=True):
		retorno = {'usuario_id':self.usuario_id.username,
				'nombre':self.usuario_id.first_name,
				'apellido':self.usuario_id.last_name,
				'password':'non displayable',
				'correo_Electronico':self.usuario_id.email}

		if not minify:
			retorno.update(
				{'telefono_celular':self.telefono_celular,
				'telefono_oficina':self.telefono_oficina,
				'telefono_casa':self.telefono_casa,
				'fecha_ingreso':self.fecha_ingreso,
				'direccion':self.direccion,
				'dedicacion':self.dedicacion,
				'estatus':self.estatus, 'jerarquia_docente': self.jerarquia_docente.pk, 'tipo_contrato': self.tipo_contrato.pk, 'centro': self.centro.pk})
		return retorno

	def get_pk(self):
		return self.usuario_id.username
		
	def toString(self):
		return self.usuario_id.first_name + ' ' + self.usuario_id.last_name 

		
class Materia(models.Model):
	codigo = models.PositiveIntegerField(unique=True)
	nombre = models.CharField(max_length=100L, unique=True)
	tipo_materia = models.CharField( max_length= 20, choices = (('Obligatoria','Obligatoria'),('Electiva','Electiva'), ('Electiva Obligatoria','Electiva Obligatoria'), ('Complementaria', 'Complementaria'), ('Laboratorio','Laboratorio')))
	unidades_credito_teoria = models.PositiveIntegerField()
	unidades_credito_practica = models.PositiveIntegerField()
	unidades_credito_laboratorio = models.PositiveIntegerField()
	estatus = models.CharField(max_length= 1, choices = (('A','Activa'), ('I','Inactiva')))
	semestre = models.PositiveIntegerField(blank=True,null=True)
	centro = models.ForeignKey(Centro)

	class Meta:
		db_table = 'materia'

	def __unicode__(self):
		return u'codigo: %d | nombre: %s | tipo_materia: %s ' % (self.codigo, self.nombre, self.tipo_materia)

	def toJson(self,minify=True):
		retorno = {'codigo':self.codigo,
				'nombre':self.nombre,
				'tipo_materia':self.tipo_materia
				}
		if not minify:
			retorno.update(
				{'unidades_credito_teoria':self.unidades_credito_teoria,
				'unidades_credito_practica':self.unidades_credito_practica,
				'unidades_credito_laboratorio':self.unidades_credito_laboratorio,
				'estatus':self.estatus,
				'semestre':self.semestre})
				
			if self.centro != None:
				retorno.update({'centro':self.centro.pk})
		return retorno
		
	def toString(self):
		return self.nombre
	
	def get_pk(self):
		return self.pk

		
class HorarioMateria(models.Model):
	dia_semana = models.CharField(max_length = 9,choices = (('Lunes','Lunes'), ('Martes','Martes'), ('Miercoles','Miercoles'), ('Jueves','Jueves'), ('Viernes','Viernes') ))
	hora_inicio = models.TimeField()
	hora_fin = models.TimeField()
	materia = models.ForeignKey('Materia')

	class Meta:
		db_table = 'horario_materia'

	def __unicode__(self):
		return u'materia: %s |dia_semana: %s | inicio: %s | fin: %s ' % (str(self. materia), self.dia_semana, convertDatetimeToString(self.hora_inicio), convertDatetimeToString(self.hora_fin))

	def toJson(self,minify=True):
		retorno = {'dia_semana':self.dia_semana,
				'hora_inicio':self.hora_inicio,
				'hora_fin':self.hora_fin
				}
		if not minify:
			if self.materia != None:
				retorno.update({'materia':self.materia.pk})
		return retorno

	def toString(self):
		return self.materia.nombre + ' ' + self.dia_semana

	def get_pk(self):
		return self.pk
		
class Programacion(models.Model):
	nombre = models.CharField(max_length=100L, unique = True)
	descripcion = models.TextField(max_length=100L, blank=True)
	fecha = models.DateField(null=True,auto_now_add=True)	
	estatus = models.CharField(max_length=8, choices = (('Aprobado','Aprobado'),('Borrador','Borrador')))
	ruta_pdf = models.CharField(max_length=100L, blank=True, unique=True, editable=False)
	periodo_lectivo = models.ForeignKey(PeriodoAcademico, db_column='periodo_lectivo', related_name='programacion_tiene_ano')

	class Meta:
		db_table = 'programacion'

	def __unicode__(self):
		return u'nombre: %s (%d-%d) | fecha_creacion: %s | estatus: %s | internal_path : %s' % 	(self.nombre, self.periodo_lectivo.periodo_lectivo,self.periodo_lectivo.semestre, convertDatetimeToString(self.fecha),self.estatus, self.ruta_pdf)

	def toJson(self,minify=True):
		retorno = {'nombre':self.nombre,
				'descripcion':self.descripcion	}
		if not minify:
			retorno.update(
				{'fecha':self.fecha,
				'estatus':self.estatus,
				'ruta_pdf':self.ruta_pdf,
				'periodo_lectivo':self.periodo_lectivo.pk})

		return retorno

	def toString(self):
		return self.nombre

	def get_pk(self):
		return self.pk
		
class ProgramacionDetalle(models.Model):
	carga = models.CharField(max_length = 1, choices = (('T','Teorica'),('P','Practica'),('C','Coordinador')))
	seccion = models.CharField(max_length=45L, blank=True)
	programacion = models.ForeignKey(Programacion)
	materia = models.ForeignKey(Materia)
	cedula = models.ForeignKey('Usuario', db_column='cedula')

	class Meta:
		db_table = 'programacion_detalle'

	def __unicode__(self):
		return u'programacion: %s | materia: %s | cedula: %s' % (str(self.programacion), str(self.materia), str(self.cedula))

	def toJson(self,minify=True):
		retorno = {'carga':self.carga,
				'seccion':self.seccion,
				'programacion':self.programacion.pk,
				'materia':self.materia.pk,
				'cedula':self.cedula.pk}

		return retorno

	def toString(self):
		return self.programacion.nombre + ' - ' + self.materia.nombre + ' - ' + self.cedula.toString()

	def get_pk(self):
		return self.pk
		
class HorarioProgramado(models.Model):
	dia_semana = models.CharField(max_length = 9,choices = (('Lunes','Lunes'), ('Martes','Martes'), ('Miercoles','Miercoles'), ('Jueves','Jueves'), ('Viernes','Viernes') ))
	hora_inicio = models.TimeField()
	hora_fin = models.TimeField()
	aula = models.ForeignKey(Aula, blank=True, null=True)
	programacion_detalle = models.ForeignKey('ProgramacionDetalle')

	class Meta:
		db_table = 'horario_programado'

	def __unicode__(self):
		return u'programacion_detalle: %s | aula: %s | dia: %s | inicio: %s | fin: %s ' % (str(self.programacion_detalle), str(self.aula), self.dia_semana, convertDatetimeToString(self.hora_inicio), convertDatetimeToString(self.hora_fin))

	def toJson(self,minify=True):
		retorno = {'dia_semana':self.dia_semana,
				'hora_inicio':self.hora_inicio,
				'hora_fin':self.hora_fin
				}
		if not minify:
			retorno.update(
				{'aula':self.aula.pk,
				'programacion_detalle':self.programacion_detalle.pk})

		return retorno

	def toString(self):
		return self.programacion_detalle.toString() + ' ' + self.dia_semana

	def get_pk(self):
		return self.pk
		
class MateriaOfertada(models.Model):
	nro_estudiantes_estimados = models.PositiveIntegerField(blank=True,null=True)
	nro_secciones_teoria = models.PositiveIntegerField(blank=True,null=True)
	nro_secciones_practica = models.PositiveIntegerField(blank=True,null=True)
	nro_secciones_laboratorio = models.PositiveIntegerField(blank=True,null=True)
	nro_preparadores1 = models.PositiveIntegerField(blank=True,null=True)
	nro_preparadores2 = models.PositiveIntegerField(blank=True,null=True)
	nro_estudiantes_inscritos = models.PositiveIntegerField(blank=True,null=True)
	periodo_academico = models.ForeignKey('PeriodoAcademico', db_column='periodo_academico', related_name='materiaofertada_tiene_anho')
	materia = models.ForeignKey(Materia)

	class Meta:
		db_table = 'materia_ofertada'

	def __unicode__(self):
		return u'materia: %s | periodo_academico: %s - %s ' % (str(self.materia.nombre), str(self.periodo_academico.semestre), str(self.periodo_academico.periodo_lectivo))

	def toJson(self,minify=True):
		retorno = {'periodo_academico':self.periodo_academico.pk,
				'materia':self.materia.pk
				}
		if not minify:
			retorno.update(
				{'nro_estudiantes_estimados':self.nro_estudiantes_estimados,
				'nro_secciones_teoria':self.nro_secciones_teoria,
				'nro_secciones_practica':self.nro_secciones_practica,
				'nro_secciones_laboratorio':self.nro_secciones_laboratorio,
				'nro_preparadores1':self.nro_preparadores1,
				'nro_preparadores2':self.nro_preparadores2,
				'nro_estudiantes_inscritos':self.nro_estudiantes_inscritos})

		return retorno

	def toString(self):
		return self.materia.nombre + ' ' + self.periodo_academico.toString()

	def get_pk(self):
		return self.pk
		
class MateriaSolicitada(models.Model):
	estatus = models.CharField(max_length=1L,choices = (('A','Aceptada'),('R','Rechazada')))
	usuario = models.ForeignKey('Usuario')
	materia = models.ForeignKey(MateriaOfertada, related_name='materiasolicitada_corresponde_materia')

	class Meta:
		db_table = 'materia_solicitada'

	def __unicode__(self):
		return u'materia: %s | usuario: %s ' % (str(self.materia), str(self.usuario))

	def toJson(self,minify=True):
		retorno = {'materia':self.materia.pk}
		if not minify:
			retorno.update(
				{'estatus':self.estatus,
				'usuario':self.usuario.pk})

		return retorno

	def toString(self):
		return self.materia.nombre + ' ' + self.materia.toString()

	def get_pk(self):
		return self.pk
		
class HorarioSolicitado(models.Model):
	dia_semana = models.CharField(max_length = 9,choices = (('Lunes','Lunes'), ('Martes','Martes'), ('Miercoles','Miercoles'), ('Jueves','Jueves'), ('Viernes','Viernes') ))
	hora_inicio = models.TimeField()
	hora_fin = models.TimeField()
	horario_solicitado = models.ForeignKey('MateriaSolicitada')
	aula = models.ForeignKey(Aula, null=True, blank=True)

	class Meta:
		db_table = 'horario_solicitado'

	def __unicode__(self):
		return u'dia: %s | inicio: %s | fin: %s | materia_solicitada: %s | aula: %s' % (self.dia_semana, convertDatetimeToString(self.hora_inicio), convertDatetimeToString(self.hora_fin), str(self.horario_solicitado), str(self.aula))

	def toJson(self,minify=True):
		retorno = {'dia_semana':self.dia_semana,
				'hora_inicio':self.hora_inicio,
				'hora_fin':self.hora_fin
				}
		if not minify:
			retorno.update(
				{'horario_solicitado':self.horario_solicitado.pk,
				'aula':self.aula.pk})

		return retorno
		
	def toString(self):
		return self.horario_solicitado.toString() + ' ' + self.dia_semana

	def get_pk(self):
		return self.pk
		
class Notificacion(models.Model):
	fecha = models.DateField(auto_now_add=True)
	asunto = models.CharField(max_length=100L)
	contenido = models.TextField()
	estatus = models.CharField(max_length=7L,editable=False, blank = True)
	usuario_emisor = models.ForeignKey('Usuario', related_name='notificacion_tiene_emisor')
	usuario_receptor = models.ForeignKey('Usuario', related_name='notificacion_tiene_receptor')

	class Meta:
		db_table = 'notificacion'

	def __unicode__(self):
		return u'usuario_emisor: %s | usuario_receptor: %s | estatus: %s | fecha: %s' % (str(self.usuario_emisor), str(self.usuario_receptor), self.estatus, convertDatetimeToString(self.fecha))

	def toJson(self,minify=True):
		retorno = {'fecha':self.fecha,
				'asunto':self.asunto
				}
		if not minify:
			retorno.update(
				{'contenido':self.contenido,
				'estatus':self.estatus,
				'usuario_emisor':self.usuario_emisor.pk,
				'usuario_receptor':self.usuario_receptor.pk})

		return retorno
	
	def toString(self):
		return ' %s  %s [ %s ] ' % (convertDatetimeToString(self.fecha), self.asunto , (lambda s : 'En transito' if not s else s )(self.estatus))

	def get_pk(self):
		return self.pk

class UsuarioRol(models.Model):
	rol = models.ForeignKey(Rol)
	cedula = models.ForeignKey(Usuario)

	class Meta:
		db_table = 'usuario_rol'

	def __unicode__(self):
		return u'usuario: %s | rol: %s' % (str(self.cedula), str(self.rol))

	def toJson(self,minify=True):
		retorno = {'rol':self.rol.pk,
				'cedula':self.cedula.pk
				}

		return retorno
		
	def toString(self):
		return self.cedula.toString() + ' ' + self.rol.nombre

	def get_pk(self):
		return self.pk