
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
		 
			for(i=0;i<respuesta.length;i++){
			
				html += '<tr><td>';
				html += respuesta[i]['name'];
				html += '</td><td style="width:100px;">';		
				html += '<button type="submit" class="btn btn-mini profesor" profesorId="profesor'+respuesta[i]['username']+'" style="margin-left:5px;float:right;">';
				html += '	<i class="icon-eye-open"></i>';
				html += '</button>';
				html += '<button type="submit" class="btn btn-mini rechazar" profesorId="profesor'+respuesta[i]['username']+'" style="margin-left:5px;float:right;">';
				html += '	<i class="icon-remove"></i>';
				html += '</button>';		
				html += '<button type="submit" class="btn btn-mini aprobar" profesorId="profesor'+respuesta[i]['username']+'" style="margin-left:5px;float:right;">';
				html += '	<i class="icon-ok"></i>';
				html += '</button></td></tr>';
				
			}
			
			if(respuesta.length = 0){
				html += '<tr><td>No hay profesores propuestos</td></tr>';
			}
			
			$('#tablaProfesores tbody').html(html);
			
			$('.profesor').click(function(){
				var elem = $('.'+$(this).attr('profesorId'));
				if(elem.hasClass('hidden')){
					elem.removeClass('hidden');
					$(this).children().removeClass('icon-eye-close');
					$(this).children().addClass('icon-eye-open');
				}else{
					elem.addClass('hidden');
					$(this).children().removeClass('icon-eye-open');
					$(this).children().addClass('icon-eye-close');
				}
			
			});
			
			$('.aprobar').click(function(){
				var elem = $('.'+$(this).attr('profesorId'));

				elem.each(function(){
				
					$(this).find('.icono').each(function(){
						if($(this).hasClass('icon-ok')){
							$(this).removeClass();
							$(this).addClass('icono');
						}else{
							$(this).removeClass();
							$(this).addClass('icono');
							$(this).addClass('icon-ok');
							$(this).css('color','green');
						}
					});
					
				});
				
			});
			
			$('.rechazar').click(function(){
				var elem = $('.'+$(this).attr('profesorId'));
				
				elem.each(function(){
				
					$(this).find('.icono').each(function(){
						if($(this).hasClass('icon-remove')){
							$(this).removeClass();
							$(this).addClass('icono');
						}else{
							$(this).removeClass();
							$(this).addClass('icono');
							$(this).addClass('icon-remove');
							$(this).css('color','red');
						}
					});
					
				});
			
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
		 
			for(i=0;i<respuesta.length;i++){
			
				html += '<tr><td>';
				html += respuesta[i]['nombre'];
				html += '</td><td style="width:30px;">';		
				html += '<button type="submit" class="btn btn-mini materia" materiaId="materia'+respuesta[i]['id']+'" style="margin-left:5px;float:right;">';
				html += '	<i class="icon-eye-open"></i>';
				html += '</button></td></tr>';
				
			}
			
			if(respuesta.length = 0){
				html += '<tr><td>No hay materias propuestas</td></tr>';
			}
			
			$('#tablaMaterias tbody').html(html);
			
			$('.materia').click(function(){
				var elem = $('.'+$(this).attr('materiaId'));
				if(elem.hasClass('hidden')){
					elem.removeClass('hidden');
					$(this).children().removeClass('icon-eye-close');
					$(this).children().addClass('icon-eye-open');
				}else{
					elem.addClass('hidden');
					$(this).children().removeClass('icon-eye-open');
					$(this).children().addClass('icon-eye-close');
				}
			
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
	
	while(dif>0){
		id = horario.dia_semana.toLowerCase()+i;
		celda = $('#'+id);
		html = '<div class="materiaHorario sol'+horario.horario_solicitado+' materia'+horario.materia_id+' profesor'+horario.username+'">';
		//html += '<i class="icono icon-ok" style="color:green;"></i>';
		//html += '<i class="icono icon-remove" style="color:red;"></i>';
		html += '<i class="icono"></i>';
		html += horario.nombre;
		html += '</div>';
		celda.append(html);

		if(celda.children().size() > 1){
			celda.addClass('conflicto');
		}
		
		i++;
		dif--;
	}
	
	html = '<h5>Profesor</h5>' + horario.usuario; 
	html += '<h5>Horario</h5>' + horario.dia_semana + ' ' + horario.hora_inicio + ' - ' + horario.hora_fin;
	
	$('.sol'+horario.horario_solicitado).popover({
		html:true,
		title:'<h5>'+horario.nombre+'</h5>',
		content:html,
		animation:true,
		trigger:'hover',
		placement:'bottom'
	 });
	
	
}
