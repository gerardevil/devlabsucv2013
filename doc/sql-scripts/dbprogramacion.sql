-- phpMyAdmin SQL Dump
-- version 4.0.5
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 13-09-2013 a las 07:45:33
-- Versión del servidor: 5.5.32-cll-lve
-- Versión de PHP: 5.2.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `dbprogramacion`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `aula`
--

CREATE TABLE IF NOT EXISTS `aula` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `aula_id` varchar(10) NOT NULL,
  `tipo_aula` varchar(1) NOT NULL,
  `capacidad` int(10) unsigned NOT NULL,
  `estatus_aula` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `aula_id` (`aula_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

--
-- Volcado de datos para la tabla `aula`
--

INSERT INTO `aula` (`id`, `aula_id`, `tipo_aula`, `capacidad`, `estatus_aula`) VALUES
(1, '11', 'I', 20, 'A'),
(2, '12', 'E', 21, 'A'),
(3, 'Oeste', 'L', 22, 'A'),
(4, '14', 'I', 20, 'I'),
(5, 'PAIII', 'I', 25, 'I'),
(6, '37', 'E', 50, 'I'),
(7, 'Este', 'L', 20, 'A');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=79 ;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add user', 3, 'add_user'),
(8, 'Can change user', 3, 'change_user'),
(9, 'Can delete user', 3, 'delete_user'),
(10, 'Can add content type', 4, 'add_contenttype'),
(11, 'Can change content type', 4, 'change_contenttype'),
(12, 'Can delete content type', 4, 'delete_contenttype'),
(13, 'Can add session', 5, 'add_session'),
(14, 'Can change session', 5, 'change_session'),
(15, 'Can delete session', 5, 'delete_session'),
(16, 'Can add site', 6, 'add_site'),
(17, 'Can change site', 6, 'change_site'),
(18, 'Can delete site', 6, 'delete_site'),
(19, 'Can add log entry', 7, 'add_logentry'),
(20, 'Can change log entry', 7, 'change_logentry'),
(21, 'Can delete log entry', 7, 'delete_logentry'),
(22, 'Can add aula', 8, 'add_aula'),
(23, 'Can change aula', 8, 'change_aula'),
(24, 'Can delete aula', 8, 'delete_aula'),
(25, 'Can add centro', 9, 'add_centro'),
(26, 'Can change centro', 9, 'change_centro'),
(27, 'Can delete centro', 9, 'delete_centro'),
(28, 'Can add periodo academico', 10, 'add_periodoacademico'),
(29, 'Can change periodo academico', 10, 'change_periodoacademico'),
(30, 'Can delete periodo academico', 10, 'delete_periodoacademico'),
(31, 'Can add propiedades sistema', 11, 'add_propiedadessistema'),
(32, 'Can change propiedades sistema', 11, 'change_propiedadessistema'),
(33, 'Can delete propiedades sistema', 11, 'delete_propiedadessistema'),
(34, 'Can add rol', 12, 'add_rol'),
(35, 'Can change rol', 12, 'change_rol'),
(36, 'Can delete rol', 12, 'delete_rol'),
(37, 'Can add tipo contrato', 13, 'add_tipocontrato'),
(38, 'Can change tipo contrato', 13, 'change_tipocontrato'),
(39, 'Can delete tipo contrato', 13, 'delete_tipocontrato'),
(40, 'Can add tipo docente', 14, 'add_tipodocente'),
(41, 'Can change tipo docente', 14, 'change_tipodocente'),
(42, 'Can delete tipo docente', 14, 'delete_tipodocente'),
(43, 'Can add jerarquia docente', 15, 'add_jerarquiadocente'),
(44, 'Can change jerarquia docente', 15, 'change_jerarquiadocente'),
(45, 'Can delete jerarquia docente', 15, 'delete_jerarquiadocente'),
(46, 'Can add usuario', 16, 'add_usuario'),
(47, 'Can change usuario', 16, 'change_usuario'),
(48, 'Can delete usuario', 16, 'delete_usuario'),
(49, 'Can add materia', 17, 'add_materia'),
(50, 'Can change materia', 17, 'change_materia'),
(51, 'Can delete materia', 17, 'delete_materia'),
(52, 'Can add horario materia', 18, 'add_horariomateria'),
(53, 'Can change horario materia', 18, 'change_horariomateria'),
(54, 'Can delete horario materia', 18, 'delete_horariomateria'),
(55, 'Can add programacion', 19, 'add_programacion'),
(56, 'Can change programacion', 19, 'change_programacion'),
(57, 'Can delete programacion', 19, 'delete_programacion'),
(58, 'Can add programacion detalle', 20, 'add_programaciondetalle'),
(59, 'Can change programacion detalle', 20, 'change_programaciondetalle'),
(60, 'Can delete programacion detalle', 20, 'delete_programaciondetalle'),
(61, 'Can add horario programado', 21, 'add_horarioprogramado'),
(62, 'Can change horario programado', 21, 'change_horarioprogramado'),
(63, 'Can delete horario programado', 21, 'delete_horarioprogramado'),
(64, 'Can add materia ofertada', 22, 'add_materiaofertada'),
(65, 'Can change materia ofertada', 22, 'change_materiaofertada'),
(66, 'Can delete materia ofertada', 22, 'delete_materiaofertada'),
(67, 'Can add materia solicitada', 23, 'add_materiasolicitada'),
(68, 'Can change materia solicitada', 23, 'change_materiasolicitada'),
(69, 'Can delete materia solicitada', 23, 'delete_materiasolicitada'),
(70, 'Can add horario solicitado', 24, 'add_horariosolicitado'),
(71, 'Can change horario solicitado', 24, 'change_horariosolicitado'),
(72, 'Can delete horario solicitado', 24, 'delete_horariosolicitado'),
(73, 'Can add notificacion', 25, 'add_notificacion'),
(74, 'Can change notificacion', 25, 'change_notificacion'),
(75, 'Can delete notificacion', 25, 'delete_notificacion'),
(76, 'Can add usuario rol', 26, 'add_usuariorol'),
(77, 'Can change usuario rol', 26, 'change_usuariorol'),
(78, 'Can delete usuario rol', 26, 'delete_usuariorol');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=15 ;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$10000$eUvNERL8S2TP$Yz1erjsnyr7sxa5wOuoivSnkgzbHavoOtnwu4TtLB2w=', '2013-09-12 14:24:51', 1, 'Admin', '', '', 'jesus.igp009@gmail.com', 1, 1, '2013-09-12 14:22:39'),
(2, 'pbkdf2_sha256$10000$6Iu6kwx7UKfW$Xjm/sxy2xof2S1jedo3vxgEAAalE1wsElZDMbcn5Pp0=', '2013-09-13 05:31:42', 0, '123456', 'Carlos', 'Acosta', 'example@domain.com', 0, 1, '2013-09-12 15:16:17'),
(3, 'pbkdf2_sha256$10000$Si5iV366iHIW$4l9qlhwIqgh7aeA5TUTPIOS22SmzugyzYvUFTMtN0Xg=', '2013-09-12 15:54:17', 0, '123457', 'Yusneyi', ' Carballo', 'example@domain.com', 0, 1, '2013-09-12 15:54:17'),
(4, 'pbkdf2_sha256$10000$ASQXRmXOSDt4$f2k3ECLUXGvq+nNnM2zcQPEUfGXSEB2CJwROD5Q1/bU=', '2013-09-12 15:55:30', 0, '123458', 'Smitt', 'Ramirez', 'example@domain.com', 0, 1, '2013-09-12 15:55:30'),
(5, 'pbkdf2_sha256$10000$HyqpqlAq2wuA$Ztj22d3ypfJnncKh3SBQNEvbcWGsg8ts5SnpRzOFmpk=', '2013-09-12 15:56:37', 0, '123459', 'Gustavo ', 'Torres', 'example@domain.com', 0, 1, '2013-09-12 15:56:37'),
(6, 'pbkdf2_sha256$10000$j75ACxYTAFym$zoiRAovEkoT6pKhx1HW2xVLx97FG4wMyvhwgQOdwSNc=', '2013-09-12 15:57:38', 0, '123460', 'Francisco', 'Sans', 'example@domain.com', 0, 1, '2013-09-12 15:57:38'),
(7, 'pbkdf2_sha256$10000$49DDFeAMyTOK$bgPeF24NKrKhM5He8eNZRgXJ2aMSJqSmkeIN5lw5pow=', '2013-09-12 15:58:42', 0, '123461', 'Sergio', 'Rivas', 'example@domain.com', 0, 1, '2013-09-12 15:58:42'),
(8, 'pbkdf2_sha256$10000$FhRUIsTuTRHb$3drttyccI5XKxs91gIOSZExLbjmMrXV9oLozn5yzakE=', '2013-09-12 15:59:38', 0, '123462', 'Jaime ', 'Parada', 'example@domain.com', 0, 1, '2013-09-12 15:59:38'),
(9, 'pbkdf2_sha256$10000$c5pvjMoQKYKZ$FLdwxo2gs0EXeajK+PIJoJG3EsrWrL46ZSejCavbFls=', '2013-09-12 16:00:59', 0, '123463', 'Wuilfredo ', 'Rangel', 'example@domain.com', 0, 1, '2013-09-12 16:00:59'),
(10, 'pbkdf2_sha256$10000$MvcmJ5XBANRK$VJ06HNRhf+iGwxrZhHwc308nIFFhB3T3ITDDVfUwnX0=', '2013-09-12 16:01:55', 0, '123464', 'Illiana ', 'Mannarino', 'example@domain.com', 0, 1, '2013-09-12 16:01:55'),
(11, 'pbkdf2_sha256$10000$L0nCs3W8E4GO$45H8+NuYa4tFX3HOYSc3wrxU8mH3ipUjt3+WdvuAizA=', '2013-09-12 16:02:59', 0, '123465', 'Rossana ', 'Diaz', 'example@domain.com', 0, 1, '2013-09-12 16:02:59'),
(12, 'pbkdf2_sha256$10000$EqMLmE7zcqYF$WJprdmXsxlrQx0he6c8rIEDzccIcgxgIZpV0SSgdrAs=', '2013-09-13 06:08:18', 0, '123450', 'Peter', 'Parker', 'example@domain.com', 0, 1, '2013-09-12 16:03:55'),
(13, 'pbkdf2_sha256$10000$5wzEQAD57Ovx$03mSy/y4UdFoYLmAYrV6EuhjYwUEHx6ha+GoC5pPNmc=', '2013-09-12 16:04:52', 0, '123451', 'Stan', 'Lee', 'example@domain.com', 0, 1, '2013-09-12 16:04:52'),
(14, 'pbkdf2_sha256$10000$gi3apWDQxlM3$z1hpkRHjaojY0A0a8yrTKkTCGE2UYQZuDkpbq1pE9eg=', '2013-09-12 16:05:39', 0, '123452', 'Bruce', 'Banner', 'example@domain.com', 0, 1, '2013-09-12 16:05:39');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `centro`
--

CREATE TABLE IF NOT EXISTS `centro` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `area` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=9 ;

--
-- Volcado de datos para la tabla `centro`
--

INSERT INTO `centro` (`id`, `nombre`, `area`) VALUES
(1, 'CICORE', 'Redes de Computadoras'),
(2, 'ISYS', 'Ingenieria de Software'),
(3, 'CISI', 'SISTEMAS DE INFORMACION Y BASES DE DATOS'),
(4, 'CCPD', 'COMPUTACIÓN PARALELA Y DISTRIBUIDA'),
(5, 'CCCT', 'CALCULO CIENTIFICO Y TECNOLOGICO'),
(6, 'CCG', 'COMPUTACION GRAFICA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=27 ;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES
(1, 'permission', 'auth', 'permission'),
(2, 'group', 'auth', 'group'),
(3, 'user', 'auth', 'user'),
(4, 'content type', 'contenttypes', 'contenttype'),
(5, 'session', 'sessions', 'session'),
(6, 'site', 'sites', 'site'),
(7, 'log entry', 'admin', 'logentry'),
(8, 'aula', 'principal', 'aula'),
(9, 'centro', 'principal', 'centro'),
(10, 'periodo academico', 'principal', 'periodoacademico'),
(11, 'propiedades sistema', 'principal', 'propiedadessistema'),
(12, 'rol', 'principal', 'rol'),
(13, 'tipo contrato', 'principal', 'tipocontrato'),
(14, 'tipo docente', 'principal', 'tipodocente'),
(15, 'jerarquia docente', 'principal', 'jerarquiadocente'),
(16, 'usuario', 'principal', 'usuario'),
(17, 'materia', 'principal', 'materia'),
(18, 'horario materia', 'principal', 'horariomateria'),
(19, 'programacion', 'principal', 'programacion'),
(20, 'programacion detalle', 'principal', 'programaciondetalle'),
(21, 'horario programado', 'principal', 'horarioprogramado'),
(22, 'materia ofertada', 'principal', 'materiaofertada'),
(23, 'materia solicitada', 'principal', 'materiasolicitada'),
(24, 'horario solicitado', 'principal', 'horariosolicitado'),
(25, 'notificacion', 'principal', 'notificacion'),
(26, 'usuario rol', 'principal', 'usuariorol');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('73bwmbgv0fm2wqr09hozl5dp3uuq1g3a', 'ZWUzMDJjMDU1YzJhZWE3MmYyZjQ5MWIzMmI2MWU2ZDhhNDE0ZGQ2NDqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==', '2013-09-26 15:47:10'),
('7ldr2h1ruz4h1yq0qd1vk0j3vscw2u1x', 'NDc0YjQ5OWQ4ZjNmYzhiMzM1YWVmNzM3NzQyYTYzZDY4MzJlMjBjMjqAAn1xAShVDV9hdXRoX3VzZXJfaWSKAQxVEl9hdXRoX3VzZXJfYmFja2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRxAlUEdXNlclgGAAAAMTIzNDUwcQN1Lg==', '2013-09-27 06:08:19'),
('96sboxs4u107dyuu0lbot6d5fytjulru', 'ZWUzMDJjMDU1YzJhZWE3MmYyZjQ5MWIzMmI2MWU2ZDhhNDE0ZGQ2NDqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==', '2013-09-27 04:31:48'),
('c0jvqhm351vwd1u9dmnkryn0s7psdemd', 'ZWUzMDJjMDU1YzJhZWE3MmYyZjQ5MWIzMmI2MWU2ZDhhNDE0ZGQ2NDqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==', '2013-09-27 04:20:29'),
('cjbpp9qdv4ub26aieu2xcktdbyt3nrim', 'ZWUzMDJjMDU1YzJhZWE3MmYyZjQ5MWIzMmI2MWU2ZDhhNDE0ZGQ2NDqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==', '2013-09-27 03:58:12'),
('fbpttjnopabz35ry00n8rtww2rmpwwdq', 'ZWUzMDJjMDU1YzJhZWE3MmYyZjQ5MWIzMmI2MWU2ZDhhNDE0ZGQ2NDqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==', '2013-09-27 04:10:02'),
('giqz1dt7resboi8qf6c88pw5npzrxed0', 'ZWUzMDJjMDU1YzJhZWE3MmYyZjQ5MWIzMmI2MWU2ZDhhNDE0ZGQ2NDqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==', '2013-09-27 04:15:55'),
('tpv5tx6pxaeb0phl6vpb38hpq5scg7nz', 'ODczZDY2YjdlYjMwM2NiNGQyMTkzMjY1YjZmNWE0ZWU5Zjc4M2ZjNjqAAn1xAShVDV9hdXRoX3VzZXJfaWSKAQJVEl9hdXRoX3VzZXJfYmFja2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRxAnUu', '2013-09-27 04:44:22'),
('v3lnsek92l7paf2ylb0s67uab8s0lr06', 'YWExMWU2YWEwMTg4NmFiY2EwYTgyZWZhZDJiYzAyOTczY2RjM2RkNjqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRxAlUNX2F1dGhfdXNlcl9pZIoBAnUu', '2013-09-27 05:03:46'),
('zc7ngi3wnwbloqlrdqkr6gp1uvptteum', 'ZWUzMDJjMDU1YzJhZWE3MmYyZjQ5MWIzMmI2MWU2ZDhhNDE0ZGQ2NDqAAn1xAShVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==', '2013-09-27 03:58:57');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_site`
--

CREATE TABLE IF NOT EXISTS `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `django_site`
--

INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(1, 'example.com', 'example.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario_materia`
--

CREATE TABLE IF NOT EXISTS `horario_materia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dia_semana` varchar(9) NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `materia_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `horario_materia_ce3d2f7b` (`materia_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=13 ;

--
-- Volcado de datos para la tabla `horario_materia`
--

INSERT INTO `horario_materia` (`id`, `dia_semana`, `hora_inicio`, `hora_fin`, `materia_id`) VALUES
(1, 'Lunes', '07:00:00', '09:00:00', 6),
(2, 'Lunes', '11:00:00', '01:00:00', 1),
(3, 'Miercoles', '11:00:00', '01:00:00', 1),
(4, 'Martes', '03:00:00', '05:00:00', 13),
(5, 'Jueves', '03:00:00', '05:00:00', 13),
(6, 'Martes', '01:00:00', '03:00:00', 7),
(7, 'Miercoles', '02:00:00', '04:00:00', 6),
(8, 'Jueves', '01:00:00', '03:00:00', 7),
(9, 'Lunes', '07:00:00', '09:00:00', 15),
(10, 'Viernes', '08:00:00', '10:00:00', 15),
(11, 'Jueves', '12:00:00', '02:00:00', 11),
(12, 'Viernes', '09:00:00', '11:00:00', 11);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario_programado`
--

CREATE TABLE IF NOT EXISTS `horario_programado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dia_semana` varchar(9) NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `aula_id` int(11) DEFAULT NULL,
  `programacion_detalle_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `horario_programado_56c2c9ef` (`aula_id`),
  KEY `horario_programado_d9bc7f1a` (`programacion_detalle_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario_solicitado`
--

CREATE TABLE IF NOT EXISTS `horario_solicitado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dia_semana` varchar(9) NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `horario_solicitado_id` int(11) NOT NULL,
  `aula_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `horario_solicitado_8a5a9aad` (`horario_solicitado_id`),
  KEY `horario_solicitado_56c2c9ef` (`aula_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=16 ;

--
-- Volcado de datos para la tabla `horario_solicitado`
--

INSERT INTO `horario_solicitado` (`id`, `dia_semana`, `hora_inicio`, `hora_fin`, `horario_solicitado_id`, `aula_id`) VALUES
(1, 'Miercoles', '07:00:00', '09:00:00', 1, 1),
(2, 'Martes', '11:00:00', '12:30:00', 2, 2),
(3, 'Miercoles', '03:30:00', '05:00:00', 3, 5),
(4, 'Jueves', '07:00:00', '09:00:00', 4, 6),
(5, 'Miercoles', '07:00:00', '08:30:00', 5, 2),
(6, 'Viernes', '08:00:00', '12:30:00', 6, 3),
(7, 'Viernes', '09:00:00', '11:00:00', 7, 4),
(8, 'Jueves', '03:15:00', '04:35:00', 8, 6),
(9, 'Lunes', '03:00:00', '05:30:00', 7, 3),
(10, 'Viernes', '11:00:00', '01:00:00', 2, 5),
(11, 'Martes', '02:00:00', '04:30:00', 5, 5),
(12, 'Martes', '01:00:00', '03:20:00', 4, 5),
(13, 'Lunes', '08:00:00', '10:20:00', 5, 7),
(14, 'Jueves', '05:00:00', '07:00:00', 1, 3),
(15, 'Miercoles', '05:00:00', '07:00:00', 6, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jerarquia_docente`
--

CREATE TABLE IF NOT EXISTS `jerarquia_docente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jerarquia` int(10) unsigned NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo_docente_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `jerarquia` (`jerarquia`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `jerarquia_docente_6e3af7da` (`tipo_docente_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Volcado de datos para la tabla `jerarquia_docente`
--

INSERT INTO `jerarquia_docente` (`id`, `jerarquia`, `nombre`, `tipo_docente_id`) VALUES
(1, 1, 'Preparador 1', 1),
(2, 2, 'Asistente Docente', 2),
(3, 3, 'Agregado', 3),
(4, 4, 'Asociado', 4),
(5, 5, 'Titular', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materia`
--

CREATE TABLE IF NOT EXISTS `materia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` int(10) unsigned NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo_materia` varchar(20) NOT NULL,
  `unidades_credito_teoria` int(10) unsigned NOT NULL,
  `unidades_credito_practica` int(10) unsigned NOT NULL,
  `unidades_credito_laboratorio` int(10) unsigned NOT NULL,
  `estatus` varchar(1) NOT NULL,
  `semestre` int(10) unsigned DEFAULT NULL,
  `centro_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `materia_f576c2aa` (`centro_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=17 ;

--
-- Volcado de datos para la tabla `materia`
--

INSERT INTO `materia` (`id`, `codigo`, `nombre`, `tipo_materia`, `unidades_credito_teoria`, `unidades_credito_practica`, `unidades_credito_laboratorio`, `estatus`, `semestre`, `centro_id`) VALUES
(1, 6201, 'Algoritmos y Programación', 'Obligatoria', 4, 1, 1, 'A', NULL, 2),
(2, 6301, 'Introducción a la Informática', 'Obligatoria', 4, 1, 1, 'A', NULL, 3),
(3, 6221, 'Aplicaciones con la Tecnología Internet', 'Obligatoria', 5, 0, 0, 'I', NULL, 3),
(4, 8601, 'Introduccion a la Computacion', 'Complementaria', 6, 0, 0, 'I', NULL, 3),
(5, 0, 'Laboratorio de Construccion de Aplicaciones Paralelas', 'Laboratorio', 0, 0, 5, 'I', NULL, 4),
(6, 6244, 'Tópicos en Computación Gráfica', 'Electiva', 5, 0, 0, 'A', NULL, 6),
(7, 6543, 'Computación de Alto Rendimiento', 'Electiva', 5, 0, 0, 'A', NULL, 4),
(8, 6022, 'Seguridad en Redes', 'Electiva', 5, 0, 0, 'A', NULL, 1),
(9, 6542, 'Modelado y Simulación de Redes', 'Electiva', 5, 0, 0, 'I', NULL, 1),
(10, 6346, 'Sistemas de BD Distribuidas', 'Electiva Obligatoria', 5, 0, 0, 'A', NULL, 3),
(11, 6040, 'Patrones de Diseño & Frameworks', 'Electiva Obligatoria', 5, 0, 0, 'A', NULL, 2),
(12, 6012, 'Redes de Computadores', 'Electiva Obligatoria', 5, 0, 0, 'A', NULL, 1),
(13, 6003, 'Comunicación de Datos', 'Obligatoria', 6, 0, 0, 'A', NULL, 1),
(15, 6109, 'Cálculo Científico', 'Obligatoria', 6, 0, 0, 'A', NULL, 5),
(16, 6134, 'Programación Matemática I', 'Electiva Obligatoria', 5, 0, 0, 'I', NULL, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materia_ofertada`
--

CREATE TABLE IF NOT EXISTS `materia_ofertada` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nro_estudiantes_estimados` int(10) unsigned DEFAULT NULL,
  `nro_secciones_teoria` int(10) unsigned DEFAULT NULL,
  `nro_secciones_practica` int(10) unsigned DEFAULT NULL,
  `nro_secciones_laboratorio` int(10) unsigned DEFAULT NULL,
  `nro_preparadores1` int(10) unsigned DEFAULT NULL,
  `nro_preparadores2` int(10) unsigned DEFAULT NULL,
  `nro_estudiantes_inscritos` int(10) unsigned DEFAULT NULL,
  `periodo_academico` int(11) NOT NULL,
  `materia_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `materia_ofertada_3495333e` (`periodo_academico`),
  KEY `materia_ofertada_ce3d2f7b` (`materia_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;

--
-- Volcado de datos para la tabla `materia_ofertada`
--

INSERT INTO `materia_ofertada` (`id`, `nro_estudiantes_estimados`, `nro_secciones_teoria`, `nro_secciones_practica`, `nro_secciones_laboratorio`, `nro_preparadores1`, `nro_preparadores2`, `nro_estudiantes_inscritos`, `periodo_academico`, `materia_id`) VALUES
(1, 90, 3, 3, 5, 2, 1, 80, 1, 12),
(2, 50, 2, 2, 3, 1, 1, 48, 1, 10),
(3, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 9),
(4, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 1),
(5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 13),
(6, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 7),
(7, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 6),
(8, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 2),
(9, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 11),
(10, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materia_solicitada`
--

CREATE TABLE IF NOT EXISTS `materia_solicitada` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `estatus` varchar(1) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `materia_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `materia_solicitada_c69e2c81` (`usuario_id`),
  KEY `materia_solicitada_ce3d2f7b` (`materia_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=9 ;

--
-- Volcado de datos para la tabla `materia_solicitada`
--

INSERT INTO `materia_solicitada` (`id`, `estatus`, `usuario_id`, `materia_id`) VALUES
(1, 'A', 2, 1),
(2, 'A', 2, 2),
(3, 'A', 12, 2),
(4, '', 3, 7),
(5, '', 5, 5),
(6, '', 10, 9),
(7, '', 4, 6),
(8, '', 7, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificacion`
--

CREATE TABLE IF NOT EXISTS `notificacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `asunto` varchar(100) NOT NULL,
  `contenido` longtext NOT NULL,
  `estatus` varchar(7) NOT NULL,
  `usuario_emisor_id` int(11) NOT NULL,
  `usuario_receptor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notificacion_747e9f81` (`usuario_emisor_id`),
  KEY `notificacion_f17977b3` (`usuario_receptor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `periodo_academico`
--

CREATE TABLE IF NOT EXISTS `periodo_academico` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `periodo_lectivo` int(10) unsigned NOT NULL,
  `semestre` int(10) unsigned NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Volcado de datos para la tabla `periodo_academico`
--

INSERT INTO `periodo_academico` (`id`, `periodo_lectivo`, `semestre`, `fecha_inicio`, `fecha_fin`) VALUES
(1, 2013, 1, '2013-01-01', '2013-07-01'),
(2, 2013, 2, '2013-07-02', '2014-02-01'),
(3, 2014, 1, '2014-01-01', '2014-07-07'),
(4, 2014, 2, '2014-07-02', '2014-02-01'),
(5, 2015, 2, '2015-01-01', '2015-07-07'),
(6, 2015, 1, '2015-01-01', '2015-07-07');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programacion`
--

CREATE TABLE IF NOT EXISTS `programacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha` date DEFAULT NULL,
  `estatus` varchar(8) NOT NULL,
  `ruta_pdf` varchar(100) NOT NULL,
  `periodo_lectivo` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  UNIQUE KEY `ruta_pdf` (`ruta_pdf`),
  KEY `programacion_afd1438f` (`periodo_lectivo`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `programacion`
--

INSERT INTO `programacion` (`id`, `nombre`, `descripcion`, `fecha`, `estatus`, `ruta_pdf`, `periodo_lectivo`) VALUES
(1, 'Prog1', '', '2013-09-12', 'Borrador', '', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programacion_detalle`
--

CREATE TABLE IF NOT EXISTS `programacion_detalle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `carga` varchar(1) NOT NULL,
  `seccion` varchar(45) NOT NULL,
  `programacion_id` int(11) NOT NULL,
  `materia_id` int(11) NOT NULL,
  `cedula` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `programacion_detalle_bdca9167` (`programacion_id`),
  KEY `programacion_detalle_ce3d2f7b` (`materia_id`),
  KEY `programacion_detalle_1a684a16` (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `propiedades_sistema`
--

CREATE TABLE IF NOT EXISTS `propiedades_sistema` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `propiedades_sistema_id` varchar(45) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `valor` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `propiedades_sistema_id` (`propiedades_sistema_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `propiedades_sistema`
--

INSERT INTO `propiedades_sistema` (`id`, `propiedades_sistema_id`, `nombre`, `valor`) VALUES
(1, '1', 'Sistema de Planificacion Docente', 'admins-1234');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE IF NOT EXISTS `rol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rol_id` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rol_id` (`rol_id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id`, `rol_id`, `nombre`, `descripcion`) VALUES
(1, 'ADMIN', 'Administrador', ''),
(2, 'JDD', 'Jefe de Departamento', ''),
(3, 'CC', 'Coordinador de Centro', ''),
(4, 'P', 'Profesor', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_contrato`
--

CREATE TABLE IF NOT EXISTS `tipo_contrato` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `tipo_contrato`
--

INSERT INTO `tipo_contrato` (`id`, `nombre`) VALUES
(2, 'Contratado/Convencional'),
(1, 'Ordinario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_docente`
--

CREATE TABLE IF NOT EXISTS `tipo_docente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Volcado de datos para la tabla `tipo_docente`
--

INSERT INTO `tipo_docente` (`id`, `nombre`) VALUES
(3, 'Agregado'),
(2, 'Asistente'),
(4, 'Asociado'),
(1, 'Instructor'),
(5, 'Titular');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id_id` int(11) NOT NULL,
  `telefono_celular` varchar(20) NOT NULL,
  `telefono_oficina` varchar(20) NOT NULL,
  `telefono_casa` varchar(20) NOT NULL,
  `fecha_ingreso` date NOT NULL,
  `direccion` longtext NOT NULL,
  `dedicacion` varchar(6) NOT NULL,
  `estatus` varchar(2) NOT NULL,
  `jerarquia_docente_id` int(11) NOT NULL,
  `tipo_contrato_id` int(11) NOT NULL,
  `centro_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id_id` (`usuario_id_id`),
  KEY `usuario_7d4d25b6` (`jerarquia_docente_id`),
  KEY `usuario_5d3c2914` (`tipo_contrato_id`),
  KEY `usuario_f576c2aa` (`centro_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=14 ;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `usuario_id_id`, `telefono_celular`, `telefono_oficina`, `telefono_casa`, `fecha_ingreso`, `direccion`, `dedicacion`, `estatus`, `jerarquia_docente_id`, `tipo_contrato_id`, `centro_id`) VALUES
(1, 2, '123', '123', '123', '2010-01-01', '', '6 hrs', 'A', 2, 2, 4),
(2, 3, '123', '123', '123', '2010-01-01', '', '6 hrs', 'A', 5, 2, 2),
(3, 4, '123', '123', '123', '2010-01-01', '', '6 hrs', 'A', 5, 2, 6),
(4, 5, '123', '123', '123', '2010-01-01', '', '6 hrs', 'A', 1, 2, 4),
(5, 6, '123', '123', '123', '2010-01-01', '', '6 hrs', 'A', 5, 2, 1),
(6, 7, '123', '123', '123', '2010-01-01', '', '6 hrs', 'A', 3, 2, 5),
(7, 8, '123', '123', '123', '2010-01-01', '', '6 hrs', 'A', 2, 2, 4),
(8, 9, '123', '123', '123', '2010-01-01', '', '6 hrs', 'A', 3, 1, 3),
(9, 10, '123', '123', '123', '2010-01-01', '', '8 hrs', 'A', 4, 2, 5),
(10, 11, '123', '123', '123', '2010-01-01', '', '12 hrs', 'A', 5, 2, 3),
(11, 12, '123', '123', '123', '2010-01-01', '', 'DE', 'I', 5, 2, 1),
(12, 13, '123', '123', '', '2010-01-01', '', 'DE', 'I', 5, 2, 1),
(13, 14, '123', '123', '', '2010-01-01', '', 'DE', 'I', 5, 2, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_rol`
--

CREATE TABLE IF NOT EXISTS `usuario_rol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rol_id` int(11) NOT NULL,
  `cedula_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_rol_b233ed9f` (`rol_id`),
  KEY `usuario_rol_1a684a16` (`cedula_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=13 ;

--
-- Volcado de datos para la tabla `usuario_rol`
--

INSERT INTO `usuario_rol` (`id`, `rol_id`, `cedula_id`) VALUES
(1, 3, 1),
(2, 3, 3),
(3, 3, 9),
(4, 1, 12),
(5, 4, 7),
(6, 3, 10),
(7, 4, 8),
(8, 2, 6),
(9, 3, 5),
(10, 4, 4),
(12, 3, 2);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `horario_materia`
--
ALTER TABLE `horario_materia`
  ADD CONSTRAINT `materia_id_refs_id_8baf9b17` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`);

--
-- Filtros para la tabla `horario_programado`
--
ALTER TABLE `horario_programado`
  ADD CONSTRAINT `aula_id_refs_id_70b30da9` FOREIGN KEY (`aula_id`) REFERENCES `aula` (`id`),
  ADD CONSTRAINT `programacion_detalle_id_refs_id_dadb05c3` FOREIGN KEY (`programacion_detalle_id`) REFERENCES `programacion_detalle` (`id`);

--
-- Filtros para la tabla `horario_solicitado`
--
ALTER TABLE `horario_solicitado`
  ADD CONSTRAINT `horario_solicitado_id_refs_id_c6173fe7` FOREIGN KEY (`horario_solicitado_id`) REFERENCES `materia_solicitada` (`id`),
  ADD CONSTRAINT `aula_id_refs_id_6474097b` FOREIGN KEY (`aula_id`) REFERENCES `aula` (`id`);

--
-- Filtros para la tabla `jerarquia_docente`
--
ALTER TABLE `jerarquia_docente`
  ADD CONSTRAINT `tipo_docente_id_refs_id_00ac7e1b` FOREIGN KEY (`tipo_docente_id`) REFERENCES `tipo_docente` (`id`);

--
-- Filtros para la tabla `materia`
--
ALTER TABLE `materia`
  ADD CONSTRAINT `centro_id_refs_id_9173bf0f` FOREIGN KEY (`centro_id`) REFERENCES `centro` (`id`);

--
-- Filtros para la tabla `materia_ofertada`
--
ALTER TABLE `materia_ofertada`
  ADD CONSTRAINT `materia_id_refs_id_73b88556` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`),
  ADD CONSTRAINT `periodo_academico_refs_id_ca963be5` FOREIGN KEY (`periodo_academico`) REFERENCES `periodo_academico` (`id`);

--
-- Filtros para la tabla `materia_solicitada`
--
ALTER TABLE `materia_solicitada`
  ADD CONSTRAINT `usuario_id_refs_id_86eb5e8a` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`),
  ADD CONSTRAINT `materia_id_refs_id_dbf4f7ef` FOREIGN KEY (`materia_id`) REFERENCES `materia_ofertada` (`id`);

--
-- Filtros para la tabla `notificacion`
--
ALTER TABLE `notificacion`
  ADD CONSTRAINT `usuario_receptor_id_refs_id_846a991a` FOREIGN KEY (`usuario_receptor_id`) REFERENCES `usuario` (`id`),
  ADD CONSTRAINT `usuario_emisor_id_refs_id_846a991a` FOREIGN KEY (`usuario_emisor_id`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `programacion`
--
ALTER TABLE `programacion`
  ADD CONSTRAINT `periodo_lectivo_refs_id_d18c3412` FOREIGN KEY (`periodo_lectivo`) REFERENCES `periodo_academico` (`id`);

--
-- Filtros para la tabla `programacion_detalle`
--
ALTER TABLE `programacion_detalle`
  ADD CONSTRAINT `programacion_id_refs_id_1787ce01` FOREIGN KEY (`programacion_id`) REFERENCES `programacion` (`id`),
  ADD CONSTRAINT `cedula_refs_id_65678694` FOREIGN KEY (`cedula`) REFERENCES `usuario` (`id`),
  ADD CONSTRAINT `materia_id_refs_id_0691dadb` FOREIGN KEY (`materia_id`) REFERENCES `materia` (`id`);

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `jerarquia_docente_id_refs_id_6f9d97b1` FOREIGN KEY (`jerarquia_docente_id`) REFERENCES `jerarquia_docente` (`id`),
  ADD CONSTRAINT `centro_id_refs_id_cc53ca7e` FOREIGN KEY (`centro_id`) REFERENCES `centro` (`id`),
  ADD CONSTRAINT `tipo_contrato_id_refs_id_c6c5017e` FOREIGN KEY (`tipo_contrato_id`) REFERENCES `tipo_contrato` (`id`),
  ADD CONSTRAINT `usuario_id_id_refs_id_0b3d7095` FOREIGN KEY (`usuario_id_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `usuario_rol`
--
ALTER TABLE `usuario_rol`
  ADD CONSTRAINT `cedula_id_refs_id_e615d985` FOREIGN KEY (`cedula_id`) REFERENCES `usuario` (`id`),
  ADD CONSTRAINT `rol_id_refs_id_979be202` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
