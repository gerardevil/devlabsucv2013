# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Aula(models.Model):
    aula_id = models.CharField(max_length=10L, primary_key=True)
    tipo_aula = models.CharField(max_length=3L)
    capacidad = models.IntegerField()
    estatus_aula = models.CharField(max_length=3L)
    class Meta:
        db_table = 'aula'
		
class Rol(models.Model):
    rol_id = models.CharField(max_length=6L, primary_key=True)
    nombre = models.CharField(max_length=100L)
    descripcion = models.CharField(max_length=500L, blank=True)
    class Meta:
        db_table = 'rol'

class TipoContrato(models.Model):
    tipo_contrato_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45L)
    class Meta:
        db_table = 'tipo_contrato'

class TipoDocente(models.Model):
    tipo_docente_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100L)
    class Meta:
        db_table = 'tipo_docente'
		
class JerarquiaDocente(models.Model):
    jerarquia_docente_id = models.IntegerField(primary_key=True)
    tipo_docente = models.ForeignKey('TipoDocente')
    nombre = models.CharField(max_length=100L)
    class Meta:
        db_table = 'jerarquia_docente'
		
class Centro(models.Model):
    centro_id = models.CharField(max_length=10L, primary_key=True)
    nombre = models.CharField(max_length=100L)
    area = models.CharField(max_length=100L)
    #usuario_id_coordinador = models.ForeignKey('Usuario', db_column='usuario_id_coordinador')
    class Meta:
        db_table = 'centro'		
		
class Usuario(models.Model):
    usuario_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100L)
    correo = models.CharField(max_length=100L)
    telefono_celular = models.CharField(max_length=20L, blank=True)
    telefono_oficina = models.CharField(max_length=20L, blank=True)
    telefono_casa = models.CharField(max_length=20L, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=500L, blank=True)
    centro = models.ForeignKey(Centro, null=True, blank=True)
    jerarquia_docente = models.ForeignKey(JerarquiaDocente, null=True, blank=True)
    tipo_contrato = models.ForeignKey(TipoContrato, null=True, blank=True)
    dedicacion = models.CharField(max_length=3L, blank=True)
    estatus = models.CharField(max_length=3L)
    clave = models.CharField(max_length=20L)
    class Meta:
        db_table = 'usuario'
		
class Materia(models.Model):
    materia_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100L)
    tipo_materia = models.CharField(max_length=100L)
    unidades_credito_teoria = models.IntegerField()
    unidades_credito_practica = models.IntegerField()
    unidades_credito_laboratorio = models.IntegerField()
    estatus = models.CharField(max_length=3L)
    semestre = models.IntegerField(null=True, blank=True)
    centro = models.ForeignKey(Centro, null=True, blank=True)
    class Meta:
        db_table = 'materia'		
		
class HorarioMateria(models.Model):
    materia = models.ForeignKey('Materia')
    dia_semana = models.CharField(max_length=50L)
    hora_inicio = models.TextField() # This field type is a guess.
    hora_fin = models.TextField() # This field type is a guess.
    class Meta:
        db_table = 'horario_materia'

class UsuarioRol(models.Model):
    cedula = models.ForeignKey(Usuario, db_column='cedula')
    rol = models.ForeignKey(Rol)
    class Meta:
        db_table = 'usuario_rol'
		

class PeriodoAcademico(models.Model):
    anho_lectivo = models.IntegerField()
    semestre = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    class Meta:
        db_table = 'periodo_academico'
		
class Programacion(models.Model):
    programacion_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100L)
    descripcion = models.CharField(max_length=100L, blank=True)
    fecha = models.DateTimeField()
    #ano_lectivo = models.ForeignKey(PeriodoAcademico, db_column='ano_lectivo')
    #semestre = models.ForeignKey(PeriodoAcademico, db_column='semestre')
    estatus = models.CharField(max_length=3L)
    ruta_pdf = models.CharField(max_length=100L, blank=True)
    class Meta:
        db_table = 'programacion'
		
class ProgramacionDetalle(models.Model):
    programacion_detalle_id = models.IntegerField(primary_key=True)
    programacion = models.ForeignKey(Programacion)
    materia = models.ForeignKey(Materia)
    cedula = models.ForeignKey('Usuario', db_column='cedula')
    carga = models.CharField(max_length=3L, blank=True)
    seccion = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'programacion_detalle'		

class HorarioProgramado(models.Model):
    programacion_detalle = models.ForeignKey('ProgramacionDetalle')
    dia_semana = models.CharField(max_length=50L)
    hora_inicio = models.TextField() # This field type is a guess.
    hora_fin = models.TextField() # This field type is a guess.
    aula = models.ForeignKey(Aula, null=True, blank=True)
    class Meta:
        db_table = 'horario_programado'
		

class MateriaOfertada(models.Model):
    #anho_periodo_academico = models.ForeignKey('PeriodoAcademico', db_column='anho_periodo_academico')
    #semestre_periodo_academico = models.ForeignKey('PeriodoAcademico', db_column='semestre_periodo_academico')
    materia = models.ForeignKey(Materia)
    nro_estudiantes_estimados = models.IntegerField()
    nro_secciones_teoria = models.IntegerField()
    nro_secciones_practica = models.IntegerField(null=True, blank=True)
    nro_secciones_laboratorio = models.IntegerField(null=True, blank=True)
    nro_preparadores1 = models.IntegerField(null=True, blank=True)
    nro_preparadores2 = models.IntegerField(null=True, blank=True)
    nro_estudiantes_inscritos = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'materia_ofertada'

class MateriaSolicitada(models.Model):
    horario_solicitado_id = models.IntegerField(primary_key=True)
    usuario = models.ForeignKey('Usuario')
    #ano_lectivo = models.ForeignKey(MateriaOfertada, db_column='ano_lectivo')
    #semestre = models.ForeignKey(MateriaOfertada, db_column='semestre')
    materia = models.ForeignKey(MateriaOfertada)
    estatus = models.CharField(max_length=3L)
    class Meta:
        db_table = 'materia_solicitada'
		
class HorarioSolicitado(models.Model):
    horario_solicitado = models.ForeignKey('MateriaSolicitada')
    dia_semana = models.CharField(max_length=50L)
    hora_inicio = models.TextField() # This field type is a guess.
    hora_fin = models.TextField() # This field type is a guess.
    aula = models.ForeignKey(Aula, null=True, blank=True)
    class Meta:
        db_table = 'horario_solicitado'
		

class Notificacion(models.Model):
    notificacion_id = models.IntegerField(primary_key=True)
    fecha = models.DateTimeField()
    #usuario_emisor = models.ForeignKey('Usuario')
    #usuario_receptor = models.ForeignKey('Usuario')
    asunto = models.CharField(max_length=100L)
    contenido = models.TextField()
    estatus = models.CharField(max_length=3L)
    class Meta:
        db_table = 'notificacion'

class PropiedadesSistema(models.Model):
    propiedades_sistema_id = models.CharField(max_length=45L, unique=True)
    nombre = models.CharField(max_length=45L)
    valor = models.CharField(max_length=45L)
    class Meta:
        db_table = 'propiedades_sistema'
