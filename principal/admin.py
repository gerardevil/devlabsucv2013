'''	Register File for add model to the admin Site, authored by The Django Book'''

from django.contrib import admin
from principal.models import Aula, Centro, PeriodoAcademico, PropiedadesSistema, Rol, TipoContrato, TipoDocente, JerarquiaDocente, Usuario, Materia, HorarioMateria, Programacion, ProgramacionDetalle, HorarioProgramado, MateriaOfertada, MateriaSolicitada, HorarioSolicitado, Notificacion, UsuarioRol

admin.site.register(Aula)
admin.site.register(Centro)
admin.site.register(PeriodoAcademico)
admin.site.register(PropiedadesSistema)
admin.site.register(Rol)
admin.site.register(TipoContrato)
admin.site.register(TipoDocente)
admin.site.register(JerarquiaDocente)
admin.site.register(Usuario)
admin.site.register(Materia)
admin.site.register(HorarioMateria)
admin.site.register(Programacion)
admin.site.register(ProgramacionDetalle)
admin.site.register(HorarioProgramado)
admin.site.register(MateriaOfertada)
admin.site.register(MateriaSolicitada)
admin.site.register(HorarioSolicitado)
admin.site.register(Notificacion)
admin.site.register(UsuarioRol)
