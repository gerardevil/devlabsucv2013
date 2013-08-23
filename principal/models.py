from __future__ import unicode_literals
from django.db import models

##########################################
# Models wich have no foreing key bellow #
##########################################


class Aula(models.Model):
	aula_id = models.CharField(max_length=10L, primary_key=True)
	tipo_aula = models.CharField(max_length=3L)
	capacidad = models.IntegerField()
	estatus_aula = models.CharField(max_length=3L)

	class Meta:
		db_table = 'aula'

	def __unicode__(self):
		return u'aula_id: %s | tipo_aula: %s | capacidad: %d | estatus_aula: %s' % (self.aula_id, self.tipo_aula, self.capacidad, self.estatus_aula)

	def toJson(self,minify=True):
		retorno = {'aula_id':self.aula_id,
				'tipo_aula':self.tipo_aula,
				'capacidad':self.capacidad,
				'estatus_aula':self.estatus_aula
				}
		return retorno

class Centro(models.Model):
	centro_id = models.CharField(max_length=10L, unique=True)
	nombre = models.CharField(max_length=100L)
	area = models.CharField(max_length=100L)

	class Meta:
		db_table = 'centro'

	def __unicode__(self):
		return u'centro_id: %s | nombre: %s | area: %s' % (self.centro_id, self.nombre, self.area)

	def toJson(self,minify=True):
		retorno = {'centro_id':self.centro_id,
				'nombre':self.nombre,
				'area':self.area
				}
		return retorno

class PeriodoAcademico(models.Model):
	anho_lectivo = models.IntegerField()
	semestre = models.IntegerField()
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField()

	class Meta:
		db_table = 'periodo_academico'

	def __unicode__(self):
		return u'anho_lectivo: %d | semestre: %d | inicio: %s | fin: %s' % (self.anho_lectivo, self.semestre, str(self.fecha_inicio), str(self.fecha_fin))

	def toJson(self,minify=True):
		retorno = {'anho_lectivo':self.anho_lectivo,
				'semestre':self.semestre,
				'fecha_inicio':self.fecha_inicio,
				'fecha_fin':self.fecha_fin
				}
		return retorno

class PropiedadesSistema(models.Model):
	propiedades_sistema_id = models.CharField(max_length=45L, unique=True)
	nombre = models.CharField(max_length=45L)
	valor = models.CharField(max_length=45L)

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

class Rol(models.Model):
	rol_id = models.CharField(max_length=6L, primary_key=True)
	nombre = models.CharField(max_length=100L)
	descripcion = models.CharField(max_length=500L, blank=True)

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

class TipoContrato(models.Model):
	tipo_contrato_id = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=45L)

	class Meta:
		db_table = 'tipo_contrato'

	def __unicode__(self):
		return u'tipo_contrato_id: %d | nombre: %s' % (self.tipo_contrato_id, self.nombre)

	def toJson(self,minify=True):
		retorno = {'tipo_contrato_id':self.tipo_contrato_id,
				'nombre':self.nombre
				}
		return retorno

class TipoDocente(models.Model):
	tipo_docente_id = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=100L)

	class Meta:
		db_table = 'tipo_docente'

	def __unicode__(self):
		return u'tipo_docente_id: %d | nombre: %s ' % (self.tipo_docente_id, self.nombre)

	def toJson(self,minify=True):
		retorno = {'tipo_docente_id':self.tipo_docente_id,
				'nombre':self.nombre
				}
		return retorno
		
class SesionActiva(models.Model):
#ALTER TABLE `sesionactiva` CHANGE `id` `id` INT( 11 ) NOT NULL AUTO_INCREMENT;
    id = models.IntegerField(primary_key=True)
    usuario = models.IntegerField(null=False)

    class Meta:
        db_table = 'sesion_activa'

    def __unicode__(self):
        return u'id: %d | usuario: %s ' % (self.id, self.usuario)

    def save(self, user): 
        try:
            foo = SesionActiva.objects.get(usuario = int(user))
        except Exception, e:
                try:
                    self.id = (SesionActiva.objects.order_by('-id')[0].id )+ 1
                except IndexError, e:
                    self.id=1         
                self.usuario = user            
                super(SesionActiva, self).save()

                
##########################################
# Models wich do have foreing key bellow #
##########################################


class JerarquiaDocente(models.Model):
	jerarquia_docente_id = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=100L)
	tipo_docente = models.ForeignKey('TipoDocente')

	class Meta:
		db_table = 'jerarquia_docente'

	def __unicode__(self):
		return u'jerarquia_docente_id: %d | nombre: %s | tipo_docente: %s' % (self.jerarquia_docente_id, self.nombre, str(self.tipo_docente))

	def toJson(self,minify=True):
		retorno = {'jerarquia_docente_id':self.jerarquia_docente_id,
				'nombre':self.nombre,
				'tipo_docente':self.tipo_docente
				}
		return retorno

class Usuario(models.Model):
	usuario_id = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=100L)
	correo = models.CharField(max_length=100L)
	telefono_celular = models.CharField(max_length=20L, blank=True)
	telefono_oficina = models.CharField(max_length=20L, blank=True)
	telefono_casa = models.CharField(max_length=20L, blank=True)
	fecha_ingreso = models.DateField(null=True, blank=True)
	direccion = models.CharField(max_length=500L, blank=True)
	dedicacion = models.CharField(max_length=3L, blank=True)
	estatus = models.CharField(max_length=3L)
	clave = models.CharField(max_length=20L)

	jerarquia_docente = models.ForeignKey(JerarquiaDocente, null=True, blank=True)
	tipo_contrato = models.ForeignKey(TipoContrato, null=True, blank=True)
	centro = models.ForeignKey(Centro)

	class Meta:
		db_table = 'usuario'

	def __unicode__(self):
		return u'usuario_id: %s | nombre: %s | clave: %s | dedicacion: %s' % (self.usuario_id, self.nombre, self.clave, self.dedicacion)

	def toJson(self,minify=True):
		retorno = {'usuario_id':self.usuario_id,
				'nombre':self.nombre,
				'correo':self.correo
				}
		if not minify:
			retorno.update(
				{'telefono_celular':self.telefono_celular,
				'telefono_oficina':self.telefono_oficina,
				'telefono_casa':self.telefono_casa,
				'fecha_ingreso':self.fecha_ingreso,
				'direccion':self.direccion,
				'dedicacion':self.dedicacion,
				'estatus':self.estatus,
				'clave':self.clave})
				
			if self.jerarquia_docente != None:
				retorno.update({'jerarquia_docente':self.jerarquia_docente.toJson(minify)})
			else:
				retorno.update({'jerarquia_docente':self.jerarquia_docente})
				
			if self.tipo_contrato != None:
				retorno.update({'tipo_contrato':self.tipo_contrato.toJson(minify)})
			else:
				retorno.update({'tipo_contrato':self.tipo_contrato})
				
			if self.centro != None:
				retorno.update({'centro':self.centro.toJson(minify)})
			else:
				retorno.update({'centro':self.centro})

		return retorno

		
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

	def __unicode__(self):
		return u'materia_id: %d | nombre: %s | tipo_materia: %s | semestre: %d' % (self.materia_id, self.nombre, self.tipo_materia, self.semestre)

	def toJson(self,minify=True):
		retorno = {'materia_id':self.materia_id,
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
				retorno.update({'centro':self.centro.toJson(minify)})
			else:
				retorno.update({'centro':self.centro})

		return retorno

		
class HorarioMateria(models.Model):
	dia_semana = models.CharField(max_length=50L)
	hora_inicio = models.TextField()
	hora_fin = models.TextField()
	materia = models.ForeignKey('Materia')

	class Meta:
		db_table = 'horario_materia'

	def __unicode__(self):
		return u'materia: %s |dia_semana: %s | inicio: %s | fin: %s ' % (str(self. materia), self.dia_semana, self.hora_inicio, self.hora_fin)

	def toJson(self,minify=True):
		retorno = {'dia_semana':self.dia_semana,
				'hora_inicio':self.hora_inicio,
				'hora_fin':self.hora_fin
				}
		if not minify:
		
			if self.materia != None:
				retorno.update({'materia':self.materia.toJson(minify)})
			else:
				retorno.update({'materia':self.materia})

		return retorno

		
class Programacion(models.Model):
	programacion_id = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=100L)
	descripcion = models.CharField(max_length=100L, blank=True)
	fecha = models.DateTimeField()
	estatus = models.CharField(max_length=3L)
	ruta_pdf = models.CharField(max_length=100L, blank=True)
	ano_lectivo = models.ForeignKey(PeriodoAcademico, db_column='ano_lectivo', related_name='programacion_tiene_ano')
	semestre = models.ForeignKey(PeriodoAcademico, db_column='semestre', related_name='programacion_tiene_semestre')

	class Meta:
		db_table = 'programacion'

	def __unicode__(self):
		return u'materia: %s |dia_semana: %s | inicio: %s | fin: %s ' % (str(self. materia), self.dia_semana, self.hora_inicio, self.hora_fin)

	def toJson(self,minify=True):
		retorno = {'programacion_id':self.programacion_id,
				'nombre':self.nombre,
				'descripcion':self.descripcion
				}
		if not minify:
			retorno.update(
				{'fecha':self.fecha,
				'estatus':self.estatus,
				'ruta_pdf':self.ruta_pdf,
				'ano_lectivo':self.ano_lectivo,
				'semestre':self.semestre})

		return retorno

		
class ProgramacionDetalle(models.Model):
	programacion_detalle_id = models.IntegerField(primary_key=True)
	carga = models.CharField(max_length=3L, blank=True)
	seccion = models.CharField(max_length=45L, blank=True)
	programacion = models.ForeignKey(Programacion)
	materia = models.ForeignKey(Materia)
	cedula = models.ForeignKey('Usuario', db_column='cedula')

	class Meta:
		db_table = 'programacion_detalle'

	def __unicode__(self):
		return u'programacion: %s | materia: %s | cedula: %s' % (str(self.programacion), str(self.materia), str(self.cedula))

	def toJson(self,minify=True):
		retorno = {'programacion_detalle_id':self.programacion_detalle_id,
				'carga':self.carga,
				'seccion':self.seccion,
				'programacion':self.programacion.toJson(minify),
				'materia':self.materia.toJson(minify),
				'cedula':self.cedula.toJson(minify)}

		return retorno

class HorarioProgramado(models.Model):
	dia_semana = models.CharField(max_length=50L)
	hora_inicio = models.TextField()
	hora_fin = models.TextField()
	aula = models.ForeignKey(Aula, null=True, blank=True)
	programacion_detalle = models.ForeignKey('ProgramacionDetalle')

	class Meta:
		db_table = 'horario_programado'

	def __unicode__(self):
		return u'programacion_detalle: %s | aula: %s | dia: %s | inicio: %s | fin: %s ' % (str(self.programacion_detalle), str(self.aula), self.dia_semana, self.hora_inicio, self.hora_fin)

	def toJson(self,minify=True):
		retorno = {'dia_semana':self.dia_semana,
				'hora_inicio':self.hora_inicio,
				'hora_fin':self.hora_fin
				}
		if not minify:
			retorno.update(
				{'aula':self.aula.toJson(minify),
				'programacion_detalle':self.programacion_detalle.toJson(minify)})

		return retorno

class MateriaOfertada(models.Model):
	nro_estudiantes_estimados = models.IntegerField()
	nro_secciones_teoria = models.IntegerField()
	nro_secciones_practica = models.IntegerField(null=True, blank=True)
	nro_secciones_laboratorio = models.IntegerField(null=True, blank=True)
	nro_preparadores1 = models.IntegerField(null=True, blank=True)
	nro_preparadores2 = models.IntegerField(null=True, blank=True)
	nro_estudiantes_inscritos = models.IntegerField(null=True, blank=True)
	anho_periodo_academico = models.ForeignKey('PeriodoAcademico', db_column='anho_periodo_academico', related_name='materiaofertada_tiene_anho')
	semestre_periodo_academico = models.ForeignKey('PeriodoAcademico', db_column='semestre_periodo_academico', related_name='materiaofertada_tiene_semestre')
	materia = models.ForeignKey(Materia)

	class Meta:
		db_table = 'materia_ofertada'

	def __unicode__(self):
		return u'materia: %s | periodo_academico: %s | anho_periodo_academico: %s' % (str(self. materia), str(self.PeriodoAcademico), str(self.anho_periodo_academico))

	def toJson(self,minify=True):
		retorno = {'anho_periodo_academico':self.anho_periodo_academico.toJson(minify),
				'semestre_periodo_academico':self.semestre_periodo_academico.toJson(minify),
				'materia':self.materia.toJson(minify)
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

class MateriaSolicitada(models.Model):
	materia_solicitada_id = models.IntegerField(primary_key=True)
	estatus = models.CharField(max_length=3L)
	usuario = models.ForeignKey('Usuario')
	ano_lectivo = models.ForeignKey(MateriaOfertada, db_column='ano_lectivo', related_name='materiasolicitada_tiene_ano')
	semestre = models.ForeignKey(MateriaOfertada, db_column='semestre', related_name='materiasolicitada_tiene_semestre')
	materia = models.ForeignKey(MateriaOfertada, related_name='materiasolicitada_corresponde_materia')

	class Meta:
		db_table = 'materia_solicitada'

	def __unicode__(self):
		return u'materia: %d | usuario: %s | anho_lectivo: %s | semestre: %s' % (str(self.materia), str(self.usuario), str(self.ano_lectivo), str(self.semestre))

	def toJson(self,minify=True):
		retorno = {'materia_solicitada_id':self.materia_solicitada_id,
				'materia':self.materia.toJson(minify)
				}
		if not minify:
			retorno.update(
				{'estatus':self.estatus,
				'usuario':self.usuario.toJson(minify),
				'ano_lectivo':self.ano_lectivo.toJson(minify),
				'semestre':self.semestre.toJson(minify)})

		return retorno

class HorarioSolicitado(models.Model):
	dia_semana = models.CharField(max_length=50L)
	hora_inicio = models.TextField()
	hora_fin = models.TextField()

	horario_solicitado = models.ForeignKey('MateriaSolicitada')
	aula = models.ForeignKey(Aula, null=True, blank=True)

	class Meta:
		db_table = 'horario_solicitado'

	def __unicode__(self):
		return u'dia: %s | inicio: %s | fin: %s | materia_solicitada: %s | aula: %s' % (self.dia_semana, self.hora_inicio, self.hora_fin, str(self.horario_solicitado), str(self.aula))

	def toJson(self,minify=True):
		retorno = {'dia_semana':self.dia_semana,
				'hora_inicio':self.hora_inicio,
				'hora_fin':self.hora_fin
				}
		if not minify:
			retorno.update(
				{'horario_solicitado':self.horario_solicitado.toJson(minify),
				'aula':self.aula.toJson(minify)})

		return retorno
		
class Notificacion(models.Model):
	notificacion_id = models.IntegerField(primary_key=True)
	fecha = models.DateTimeField()
	asunto = models.CharField(max_length=100L)
	contenido = models.TextField()
	estatus = models.CharField(max_length=3L)
	usuario_emisor = models.ForeignKey('Usuario', related_name='notificacion_tiene_emisor')
	usuario_receptor = models.ForeignKey('Usuario', related_name='notificacion_tiene_receptor')

	class Meta:
		db_table = 'notificacion'

	def __unicode__(self):
		return u'usuario_emisor: %s | usuario_receptor: %s | estatus: %s | fecha: %s' % (str(self.usuario_emisor), str(self.usuario_receptor), self.estatus, str(self.fecha))

	def toJson(self,minify=True):
		retorno = {'notificacion_id':self.notificacion_id,
				'fecha':self.fecha,
				'asunto':self.asunto
				}
		if not minify:
			retorno.update(
				{'contenido':self.contenido,
				'estatus':self.estatus,
				'usuario_emisor':self.usuario_emisor.toJson(minify),
				'usuario_receptor':self.usuario_receptor.toJson(minify)})

		return retorno

class UsuarioRol(models.Model):
	rol = models.ForeignKey(Rol)
	cedula = models.ForeignKey(Usuario, db_column='cedula')

	class Meta:
		db_table = 'usuario_rol'

	def __unicode__(self):
		return u'usuario: %s | rol: %s' % (str(self.cedula), str(self.rol))

	def toJson(self,minify=True):
		retorno = {'rol':self.rol.toJson(minify),
				'cedula':self.cedula.toJson(minify)
				}

		return retorno