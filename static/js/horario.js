
$(function(){
	
	$('#tablaProfesores tbody').html('<tr><td>Cargando...</td></tr>');
	$('#tablaMaterias tbody').html('<tr><td>Cargando...</td></tr>');
	cargarHorario();
	cargarProfesores();
	cargarMaterias();

	$(".nano").nanoScroller({ preventPageScrolling: true });
	$(".submenu").addClass("hidden");
	$(".pane").css("display","block");
	$(".slider").css("display","block");
});



function cargarHorario(){

	$('.materiaHorario').remove();
	$('#tablaHorario td').removeClass();
	
	$('#tablaHorario').hideLoading();
	$('#tablaHorario').showLoading({'indicatorZIndex' : 101,'overlayZIndex': 100});
	
	if ( ~$('#rol_usuario').text().indexOf('Coordinador(a)') )
	{
		var url = '/schedulexrequest/cc';
	}else if(~$('#rol_usuario').text().indexOf('Jefe(a) de Departamento')){

		var url = '/schedulexrequest/jdd';
	}else{
		console.error($('#rol_usuario').text()+" is not a valid rol");
	}
	
	var param = '';
	
	$.ajax({  
		 type: 'GET',  
		 url: url,
		 dataType: 'json',
		 //data: param,
		 success: function(respuesta){
		 
			try{
			
				for(i=0;i<respuesta.length;i++){
				
					insertarMateriaHorario(respuesta[i]);
					
				}
			
			}catch(ex){
				console.error(ex.name + " - "+ex.message);
			}
			
		 },
		 complete: function(){
			$('#tablaHorario').hideLoading();
		 },
		 error: function(xhr,errmsg,err){
			//console.error(xhr.status + ": " + xhr.responseText);
		 }
		});
}

function cargarProfesores(){

	$('#tablaProfesores').hideLoading();
	$('#tablaProfesores').showLoading();

	if ( ~$('#rol_usuario').text().indexOf('Coordinador(a)') )
	{
		var url = '/userxcenter';
	}else if(~$('#rol_usuario').text().indexOf('Jefe(a) de Departamento')){

		var url = '/userxcenterall';
	}else{
		console.error($('#rol_usuario').text()+" is not a valid rol");
	}	

	var param = '';
	
	$.ajax({  
		 type: 'GET',  
		 url: url,
		 dataType: 'json',
		 //data: param,
		 success: function(respuesta){
		 
			var html = '';
			$('#tablaProfesores tbody').html('');
		 
			for(i=0;i<respuesta.length;i++){
			
				html = '<tr><td>';
				html += respuesta[i]['name'];
				html += '</td><td style="width:100px;">';		
				html += '<button id="botonP'+i+'" type="submit" class="btn btn-mini profesor" style="margin-left:5px;float:right;">';
				html += '	<i class="icon-eye-open"></i>';
				html += '</button>';
				html += '<button id="botonR'+i+'" type="submit" class="btn btn-mini rechazar" style="margin-left:5px;float:right;">';
				html += '	<i class="icon-remove"></i>';
				html += '</button>';		
				html += '<button id="botonA'+i+'" type="submit" class="btn btn-mini aprobar" style="margin-left:5px;float:right;">';
				html += '	<i class="icon-ok"></i>';
				html += '</button></td></tr>';
				
				$('#tablaProfesores tbody').append(html);
				$('#botonP'+i).data('profesor',respuesta[i]['username']);
				$('#botonR'+i).data('profesor',respuesta[i]['username']);
				$('#botonA'+i).data('profesor',respuesta[i]['username']);
				
			}
			
			if(respuesta.length = 0){
				html += '<tr><td>No hay profesores propuestos</td></tr>';
			}
			
			
			
			$('.profesor').click(function(){
			
				var boton = $(this);
				
				$('.materiaHorario').each(function(){
				
					if($(this).data('profesor') == boton.data('profesor')){
					
						var elem = $(this);
					
						if(elem.hasClass('hidden')){
							elem.removeClass('hidden');
							boton.children().removeClass('icon-eye-close');
							boton.children().addClass('icon-eye-open');
						}else{
							elem.addClass('hidden');
							boton.children().removeClass('icon-eye-open');
							boton.children().addClass('icon-eye-close');
						}
					
					}
				
				});
			
			});
			
			$('.aprobar').click(function(){
				
				var boton = $(this);
				
				$('.materiaHorario').each(function(){
				
					if($(this).data('profesor') == boton.data('profesor')){
					
						var elem = $(this).find('.icono');
					
						if(elem.hasClass('icon-ok')){
							elem.removeClass();
							elem.addClass('icono');
							$(this).data('estatus','P');
						}else{
							elem.removeClass();
							elem.addClass('icono');
							elem.addClass('icon-ok');
							elem.css('color','green');
							$(this).data('estatus','AC');
						}
					
					}
				
				});
				
			});
			
			$('.rechazar').click(function(){
				
				var boton = $(this);
				var flag = false;
				var conflicts = new Array();
				
				$('.materiaHorario').each(function(){
				
					if($(this).data('profesor') == boton.data('profesor')){
					
						var elem = $(this).find('.icono');
						
					
						if(elem.hasClass('icon-remove')){
							elem.removeClass();
							elem.addClass('icono');
							$(this).data('estatus','P');
						}else{
							elem.removeClass();
							elem.addClass('icono');
							elem.addClass('icon-remove');
							elem.css('color','red');
							$(this).data('estatus','RC');
							if (!flag)
								flag=true;
						}
						
						if($(this).parent().hasClass('conflicto')){
							if(conflicts.indexOf($(this).data('timeperiod'))<0){
								conflicts.push($(this).data('timeperiod'));
							}
						}
						
					}
				
				});
				
				if(flag){

					$.ajax({  
						type: 'GET',  
						url: '/getemailunique',
						dataType: 'text',
						data: {
							'user': 'profesor'+boton.data('profesor').toString(),
						},
						success: function(email){
							var content = "";
							if (conflicts.length)
								content = "[!] El Sistema ha detectado conflicto en las siguientes propuestas:\n\n"+conflicts.join("\n");
							$('#modalContacto .modal-body #emailForm #asunto #matter').val("[Cambio de Estatus de Propuesta]");
							$('#modalContacto .modal-body #emailForm #destinatarios #to').val(email+";");//to format is allways {email;}
							$('#modalContacto .modal-body #emailForm #contenido #content').val(content);           
							$('#modalContacto').modal('show');							
						},
						error: function(xhr,errmsg,err){
							console.error(xhr.status + ": " + xhr.responseText);
						}
					});
				}

				
			});
			
		 },
		 complete: function(){
			$('#tablaProfesores').hideLoading();
		 },
		 error: function(xhr,errmsg,err){
			$('#tablaProfesores tbody').html('<tr><td>Error al cargar los profesores</td></tr>');
			//console.error(xhr.status + ": " + xhr.responseText);
		 }
		});

}

function cargarMaterias(){

	$('#tablaMaterias').hideLoading();
	$('#tablaMaterias').showLoading();

	if ( ~$('#rol_usuario').text().indexOf('Coordinador(a)') )
	{
		var url = '/subjectxrequest';
	}else if(~$('#rol_usuario').text().indexOf('Jefe(a) de Departamento')){

		var url = '/subjectxrequestall';
	}else{
		console.error($('#rol_usuario').text()+" is not a valid rol");
	}	

	var param = '';
	
	$.ajax({  
		 type: 'GET',  
		 url: url,
		 dataType: 'json',
		 //data: param,
		 success: function(respuesta){
		 
			var html = '';
			
			$('#tablaMaterias tbody').html('');
		 
			for(i=0;i<respuesta.length;i++){
			
				html = '<tr><td>';
				html += respuesta[i]['nombre'];
				html += '</td><td style="width:30px;">';		
				html += '<button id="botonM'+i+'" type="submit" class="btn btn-mini materia" style="margin-left:5px;float:right;">';
				html += '	<i class="icon-eye-open"></i>';
				html += '</button></td></tr>';
				
				$('#tablaMaterias tbody').append(html);
				$('#botonM'+i).data('materia',respuesta[i]['id']);
				
			}
			
			if(respuesta.length = 0){
				html += '<tr><td>No hay materias propuestas</td></tr>';
			}
			
			
			
			$('.materia').click(function(){

				var boton = $(this);
				
				$('.materiaHorario').each(function(){
				
					if($(this).data('materia') == boton.data('materia')){
					
						var elem = $(this);
					
						if(elem.hasClass('hidden')){
							elem.removeClass('hidden');
							boton.children().removeClass('icon-eye-close');
							boton.children().addClass('icon-eye-open');
						}else{
							elem.addClass('hidden');
							boton.children().removeClass('icon-eye-open');
							boton.children().addClass('icon-eye-close');
						}
					
					}
				
				});
			});
		 },
		 complete: function(){
			$('#tablaMaterias').hideLoading();
		 },
		 error: function(xhr,errmsg,err){
			$('#tablaMaterias tbody').html('<tr><td>Error al cargar las materias</td></tr>');
			//console.error(xhr.status + ": " + xhr.responseText);
		 }
		});

}

function insertarMateriaHorario(horario){

	var horaIni = new Date('01/01/2012 '+horario.hora_inicio);
	var horaFin = new Date('01/01/2012 '+horario.hora_fin);
	
	var id;
	var celda;
	var i = horaIni.getHours();
	
	if(horaFin.getHours() < horaIni.getHours()) horaFin.setHours(horaFin.getHours()+12);
	
	//console.log('horaIni: '+horaIni.getHours());
	//console.log('horaFin: '+horaFin.getHours());
	
	var dif = (horaFin.getTime()-horaIni.getTime())/1000/60/60;
	
	//console.log(dif);
	
	var html = '';
	var idMateriaHorario = $('.materiaHorario').size();
	
	
	while(dif>0){
		id = horario.dia_semana.toLowerCase()+i;
		celda = $('#'+id);
		estatus = '';
		html = '<div id="materia'+idMateriaHorario+'" class="materiaHorario">';
		if(horario.estatus == 'AC'){
			html += '<i class="icono icon-ok" style="color:green;"></i>';
			estatus = 'Aceptada por Coordinador de Centro';
		}else if(horario.estatus == 'RC'){
			html += '<i class="icono icon-remove" style="color:red;"></i>';
			estatus = 'Rechazada por Coordinador de Centro';
		}else if(horario.estatus == 'AJ'){
			html += '<i class="icono icon-ok" style="color:green;"></i>';
			estatus = 'Aceptada por Jefe Departamento';
		}else if(horario.estatus == 'RJ'){
			html += '<i class="icono icon-remove" style="color:red;"></i>';
			estatus = 'Rechazada por Jefe Departamento';
		}else if(horario.estatus == 'PJ'){
			html += '<i class="icono icon-ok" style="color:green;"></i>';
			estatus = 'Procesando por Jefe Departamento';
		}else if(horario.estatus == 'P'){
			html += '<i class="icono"></i>';
			estatus = 'Procesando';
		}else{
			html += '<i class="icono"></i>';
		}
		html += horario.nombre;
		html += '</div>';
		celda.append(html);

		$('#materia'+idMateriaHorario).data('solicitud',horario.materia_solicitada);
		$('#materia'+idMateriaHorario).data('materia',horario.materia_id);
		$('#materia'+idMateriaHorario).data('profesor',horario.username);
		$('#materia'+idMateriaHorario).data('estatus',horario.estatus);
		$('#materia'+idMateriaHorario).data('timeperiod',horario.nombre+'-['+horario.dia_semana+']'+horario.hora_inicio+'-'+horario.hora_fin);
		
		if(celda.children().size() > 1){
			celda.addClass('conflicto');
		}
		
		html = '<h5>Profesor</h5>' + horario.usuario; 
		html += '<h5>Horario</h5>' + horario.dia_semana + ' ' + horario.hora_inicio + ' - ' + horario.hora_fin;
		
		
		
		html += '<h5>Estatus</h5>' + estatus;
		
		$('#materia'+idMateriaHorario).popover({
			html:true,
			title:'<h5>'+horario.nombre+'</h5>',
			content:html,
			animation:true,
			trigger:'hover',
			placement:'bottom'
		 });
		 
		
		i++;
		dif--;
		idMateriaHorario++;
	}
	
	
	
	
}

function guardarHorario(){
	
	var datos = {};
	var aux2 = new Array();
	
	$('.materiaHorario').each(function(index){
		
		if(aux2.indexOf($(this).data('solicitud')) < 0){
			
			datos[$(this).data('solicitud')]=$(this).data('estatus');
			aux2.push($(this).data('solicitud'));
		}
	
	});
	
	$('#tablaHorario').hideLoading();
	$('#tablaHorario').showLoading({'indicatorZIndex' : 101,'overlayZIndex': 100});
	
	param = 'data='+JSON.stringify(datos);
	
	//alert(param);
	
	$.ajax({  
		 type: 'POST',  
		 url: '/changestatus',
		 data: param,
		 success: function(res){
			var html = '<div class="alert alert-success" style="width:70%" >';
			html += '<button type="button" class="close" data-dismiss="alert">&times;</button>';
			html += 'Horario de solicitudes guardado satisfactoriamente.</div>';
			
			$('#saveButton').parent().prepend(html);
			
			cargarHorario();
			
		 },
		 complete: function(){
			$('#tablaHorario').hideLoading();
		 },
		 error: function(xhr,errmsg,err){
			console.error(xhr.status + ": " + xhr.responseText);
		 }
		});

}



function enviarHorario(){
	
	var datos = {};
	var aux2 = new Array();
	
	$('.materiaHorario').each(function(index){
		
		if(aux2.indexOf($(this).data('solicitud')) < 0 && $(this).data('estatus')=='AC'){
			
			datos[$(this).data('solicitud')]='PJ';
			aux2.push($(this).data('solicitud'));
		}
	
	});
	
	$('#tablaHorario').hideLoading();
	$('#tablaHorario').showLoading({'indicatorZIndex' : 101,'overlayZIndex': 100});
	
	param = 'data='+JSON.stringify(datos);
	
	//alert(param);
	
	$.ajax({  
		 type: 'POST',  
		 url: '/changestatus',
		 data: param,
		 success: function(res){
			var html = '<div class="alert alert-success" style="width:70%" >';
			html += '<button type="button" class="close" data-dismiss="alert">&times;</button>';
			html += 'Horario de solicitudes enviado al Jefe de Departamento.</div>';
			
			$('#saveButton').parent().prepend(html);
			
			cargarHorario();
		 },
		 complete: function(){
			$('#tablaHorario').hideLoading();
		 },
		 error: function(xhr,errmsg,err){
			console.error(xhr.status + ": " + xhr.responseText);
		 }
		});

}