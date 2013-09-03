BEGIN;
CREATE TABLE `aula` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `aula_id` varchar(10) NOT NULL UNIQUE,
    `tipo_aula` varchar(1) NOT NULL,
    `capacidad` integer UNSIGNED NOT NULL,
    `estatus_aula` varchar(1) NOT NULL
)
;
CREATE TABLE `centro` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `nombre` varchar(100) NOT NULL UNIQUE,
    `area` varchar(100) NOT NULL
)
;
CREATE TABLE `periodo_academico` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `periodo_lectivo` integer UNSIGNED NOT NULL,
    `semestre` integer UNSIGNED NOT NULL,
    `fecha_inicio` date NOT NULL,
    `fecha_fin` date NOT NULL
)
;
CREATE TABLE `propiedades_sistema` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `propiedades_sistema_id` varchar(45) NOT NULL UNIQUE,
    `nombre` varchar(45) NOT NULL,
    `valor` varchar(45) NOT NULL
)
;
CREATE TABLE `rol` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `rol_id` varchar(20) NOT NULL UNIQUE,
    `nombre` varchar(100) NOT NULL UNIQUE,
    `descripcion` longtext NOT NULL
)
;
CREATE TABLE `tipo_contrato` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `nombre` varchar(45) NOT NULL UNIQUE
)
;
CREATE TABLE `tipo_docente` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `nombre` varchar(100) NOT NULL UNIQUE
)
;
CREATE TABLE `jerarquia_docente` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `jerarquia` integer UNSIGNED NOT NULL UNIQUE,
    `nombre` varchar(100) NOT NULL UNIQUE,
    `tipo_docente_id` integer NOT NULL
)
;
ALTER TABLE `jerarquia_docente` ADD CONSTRAINT `tipo_docente_id_refs_id_00ac7e1b` FOREIGN KEY (`tipo_docente_id`) REFERENCES `tipo_docente` (`id`);
CREATE TABLE `usuario` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `usuario_id_id` integer NOT NULL UNIQUE,
    `telefono_celular` varchar(20) NOT NULL,
    `telefono_oficina` varchar(20) NOT NULL,
    `telefono_casa` varchar(20) NOT NULL,
    `fecha_ingreso` date NOT NULL,
    `direccion` longtext NOT NULL,
    `dedicacion` varchar(6) NOT NULL,
    `estatus` varchar(2) NOT NULL,
    `jerarquia_docente_id` integer NOT NULL,
    `tipo_contrato_id` integer NOT NULL,
    `centro_id` integer NOT NULL
)
;
ALTER TABLE `usuario` ADD CONSTRAINT `tipo_contrato_id_refs_id_c6c5017e` FOREIGN KEY (`tipo_contrato_id`) REFERENCES `tipo_contrato` (`id`);
ALTER TABLE `usuario` ADD CONSTRAINT `centro_id_refs_id_cc53ca7e` FOREIGN KEY (`centro_id`) REFERENCES `centro` (`id`);
ALTER TABLE `usuario` ADD CONSTRAINT `jerarquia_docente_id_refs_id_6f9d97b1` FOREIGN KEY (`jerarquia_docente_id`) REFERENCES `jerarquia_docente` (`id`);
ALTER TABLE `usuario` ADD CONSTRAINT `usuario_id_id_refs_id_0b3d7095` FOREIGN KEY (`usuario_id_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `materia` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `codigo` integer UNSIGNED NOT NULL UNIQUE,
    `nombre` varchar(100) NOT NULL UNIQUE,
    `tipo_materia` varchar(20) NOT NULL,
    `unidades_credito_teoria` integer UNSIGNED NOT NULL,
    `unidades_credito_practica` integer UNSIGNED NOT NULL,
    `unidades_credito_laboratorio` integer UNSIGNED NOT NULL,
    `estatus` varchar(1) NOT NULL,
    `semestre` integer UNSIGNED,
    `centro_id` integer NOT NULL
)
;
ALTER TABLE `materia` ADD CONSTRAINT `centro_id_refs_id_9173bf0f` FOREIGN KEY (`centro_id`) REFERENCES `centro` (`id`);
CREATE TABLE `horario_materia` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `dia_semana` varchar(9) NOT NULL,
    `hora_inicio` time NOT NULL,
    `hora_fin` time NOT NULL,
    `materia_id` integer NOT NULL
)
;
ALTER TABLE `horario_materia` ADD CONSTRAINT `materia_id_refs_id_8baf9b17` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`);
CREATE TABLE `programacion` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `nombre` varchar(100) NOT NULL UNIQUE,
    `descripcion` longtext NOT NULL,
    `fecha` date,
    `estatus` varchar(8) NOT NULL,
    `ruta_pdf` varchar(100) NOT NULL UNIQUE,
    `periodo_lectivo` integer NOT NULL
)
;
ALTER TABLE `programacion` ADD CONSTRAINT `periodo_lectivo_refs_id_d18c3412` FOREIGN KEY (`periodo_lectivo`) REFERENCES `periodo_academico` (`id`);
CREATE TABLE `programacion_detalle` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `carga` varchar(1) NOT NULL,
    `seccion` varchar(45) NOT NULL,
    `programacion_id` integer NOT NULL,
    `materia_id` integer NOT NULL,
    `cedula` integer NOT NULL
)
;
ALTER TABLE `programacion_detalle` ADD CONSTRAINT `cedula_refs_id_65678694` FOREIGN KEY (`cedula`) REFERENCES `usuario` (`id`);
ALTER TABLE `programacion_detalle` ADD CONSTRAINT `materia_id_refs_id_0691dadb` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`);
ALTER TABLE `programacion_detalle` ADD CONSTRAINT `programacion_id_refs_id_1787ce01` FOREIGN KEY (`programacion_id`) REFERENCES `programacion` (`id`);
CREATE TABLE `horario_programado` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `dia_semana` varchar(9) NOT NULL,
    `hora_inicio` time NOT NULL,
    `hora_fin` time NOT NULL,
    `aula_id` integer,
    `programacion_detalle_id` integer NOT NULL
)
;
ALTER TABLE `horario_programado` ADD CONSTRAINT `programacion_detalle_id_refs_id_dadb05c3` FOREIGN KEY (`programacion_detalle_id`) REFERENCES `programacion_detalle` (`id`);
ALTER TABLE `horario_programado` ADD CONSTRAINT `aula_id_refs_id_70b30da9` FOREIGN KEY (`aula_id`) REFERENCES `aula` (`id`);
CREATE TABLE `materia_ofertada` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `nro_estudiantes_estimados` integer UNSIGNED NOT NULL,
    `nro_secciones_teoria` integer UNSIGNED NOT NULL,
    `nro_secciones_practica` integer UNSIGNED NOT NULL,
    `nro_secciones_laboratorio` integer UNSIGNED NOT NULL,
    `nro_preparadores1` integer UNSIGNED NOT NULL,
    `nro_preparadores2` integer UNSIGNED NOT NULL,
    `nro_estudiantes_inscritos` integer UNSIGNED NOT NULL,
    `periodo_academico` integer NOT NULL,
    `materia_id` integer NOT NULL
)
;
ALTER TABLE `materia_ofertada` ADD CONSTRAINT `periodo_academico_refs_id_ca963be5` FOREIGN KEY (`periodo_academico`) REFERENCES `periodo_academico` (`id`);
ALTER TABLE `materia_ofertada` ADD CONSTRAINT `materia_id_refs_id_73b88556` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`);
CREATE TABLE `materia_solicitada` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `estatus` varchar(1) NOT NULL,
    `usuario_id` integer NOT NULL,
    `materia_id` integer NOT NULL
)
;
ALTER TABLE `materia_solicitada` ADD CONSTRAINT `usuario_id_refs_id_86eb5e8a` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);
ALTER TABLE `materia_solicitada` ADD CONSTRAINT `materia_id_refs_id_dbf4f7ef` FOREIGN KEY (`materia_id`) REFERENCES `materia_ofertada` (`id`);
CREATE TABLE `horario_solicitado` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `dia_semana` varchar(9) NOT NULL,
    `hora_inicio` time NOT NULL,
    `hora_fin` time NOT NULL,
    `horario_solicitado_id` integer NOT NULL,
    `aula_id` integer
)
;
ALTER TABLE `horario_solicitado` ADD CONSTRAINT `horario_solicitado_id_refs_id_c6173fe7` FOREIGN KEY (`horario_solicitado_id`) REFERENCES `materia_solicitada` (`id`);
ALTER TABLE `horario_solicitado` ADD CONSTRAINT `aula_id_refs_id_6474097b` FOREIGN KEY (`aula_id`) REFERENCES `aula` (`id`);
CREATE TABLE `notificacion` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `fecha` date NOT NULL,
    `asunto` varchar(100) NOT NULL,
    `contenido` longtext NOT NULL,
    `estatus` varchar(7) NOT NULL,
    `usuario_emisor_id` integer NOT NULL,
    `usuario_receptor_id` integer NOT NULL
)
;
ALTER TABLE `notificacion` ADD CONSTRAINT `usuario_emisor_id_refs_id_846a991a` FOREIGN KEY (`usuario_emisor_id`) REFERENCES `usuario` (`id`);
ALTER TABLE `notificacion` ADD CONSTRAINT `usuario_receptor_id_refs_id_846a991a` FOREIGN KEY (`usuario_receptor_id`) REFERENCES `usuario` (`id`);
CREATE TABLE `usuario_rol` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `rol_id` integer NOT NULL,
    `cedula` integer NOT NULL
)
;
ALTER TABLE `usuario_rol` ADD CONSTRAINT `rol_id_refs_id_979be202` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`);
ALTER TABLE `usuario_rol` ADD CONSTRAINT `cedula_refs_id_e615d985` FOREIGN KEY (`cedula`) REFERENCES `usuario` (`id`);
CREATE INDEX `jerarquia_docente_6e3af7da` ON `jerarquia_docente` (`tipo_docente_id`);
CREATE INDEX `usuario_7d4d25b6` ON `usuario` (`jerarquia_docente_id`);
CREATE INDEX `usuario_5d3c2914` ON `usuario` (`tipo_contrato_id`);
CREATE INDEX `usuario_f576c2aa` ON `usuario` (`centro_id`);
CREATE INDEX `materia_f576c2aa` ON `materia` (`centro_id`);
CREATE INDEX `horario_materia_ce3d2f7b` ON `horario_materia` (`materia_id`);
CREATE INDEX `programacion_afd1438f` ON `programacion` (`periodo_lectivo`);
CREATE INDEX `programacion_detalle_bdca9167` ON `programacion_detalle` (`programacion_id`);
CREATE INDEX `programacion_detalle_ce3d2f7b` ON `programacion_detalle` (`materia_id`);
CREATE INDEX `programacion_detalle_1a684a16` ON `programacion_detalle` (`cedula`);
CREATE INDEX `horario_programado_56c2c9ef` ON `horario_programado` (`aula_id`);
CREATE INDEX `horario_programado_d9bc7f1a` ON `horario_programado` (`programacion_detalle_id`);
CREATE INDEX `materia_ofertada_3495333e` ON `materia_ofertada` (`periodo_academico`);
CREATE INDEX `materia_ofertada_ce3d2f7b` ON `materia_ofertada` (`materia_id`);
CREATE INDEX `materia_solicitada_c69e2c81` ON `materia_solicitada` (`usuario_id`);
CREATE INDEX `materia_solicitada_ce3d2f7b` ON `materia_solicitada` (`materia_id`);
CREATE INDEX `horario_solicitado_8a5a9aad` ON `horario_solicitado` (`horario_solicitado_id`);
CREATE INDEX `horario_solicitado_56c2c9ef` ON `horario_solicitado` (`aula_id`);
CREATE INDEX `notificacion_747e9f81` ON `notificacion` (`usuario_emisor_id`);
CREATE INDEX `notificacion_f17977b3` ON `notificacion` (`usuario_receptor_id`);
CREATE INDEX `usuario_rol_b233ed9f` ON `usuario_rol` (`rol_id`);
CREATE INDEX `usuario_rol_1a684a16` ON `usuario_rol` (`cedula`);

COMMIT;
