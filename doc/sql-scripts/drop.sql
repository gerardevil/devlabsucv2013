
# For this instance SET this CHECK attribute of MySQL to allow deleting all the DB whitout
# any constraint error
SET FOREIGN_KEY_CHECKS = 0;

#DROP table which do not have any constraints
drop table if exists materia_solicitada,horario_solicitado,notificacion,propiedades_sistema,horario_materia,usuario_rol,programacion_detalle,horario_programado;

#Now DROP all table wich use constraints
drop table if exists rol;
drop table if exists materia_ofertada; 
drop table if exists materia; 
drop table if exists programacion;
drop table if exists periodo_academico;
drop table if exists aula;
drop table if exists usuario; 
drop table if exists jerarquia_docente; 
drop table if exists tipo_contrato; 
drop table if exists centro; 
drop table if exists tipo_docente; 

#Reset this attribute for correct function of the DB
SET FOREIGN_KEY_CHECKS = 1;