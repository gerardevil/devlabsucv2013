
$(function(){

	$(".nano").nanoScroller();
	$(".submenu").addClass("hidden");
	$(".pane").css("display","block");
	$(".slider").css("display","block");
	$('#tablaProfesores tbody').html('<tr><td>Cargando...</td></tr>');
	$('#tablaMaterias tbody').html('<tr><td>Cargando...</td></tr>');
	cargarHorario();
	cargarProfesores();
	cargarMaterias();
});



function cargarHorario(){

	$('#tablaHorario').hideLoading();
	$('#tablaHorario').showLoading({'indicatorZIndex' : 101,'overlayZIndex': 100});
	
	var url = '/schedulexrequest/cc';
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
	
	var url = '/userxcenter';
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
				html += '<button type="submit" class="btn btn-mini" style="margin-left:5px;float:right;">';
				html += '	<i class="icon-remove"></i>';
				html += '</button>';		
				html += '<button type="submit" class="btn btn-mini" style="margin-left:5px;float:right;">';
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
	
	var url = '/subjectxrequest';
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
	
	var dif = (horaFin.getTime()-horaIni.getTime())/1000/60/60;
	
	var id;
	var celda;
	var i = horaIni.getHours();
	
	while(dif>0){
		id = horario.dia_semana.toLowerCase()+i;
		celda = $('#'+id);
		celda.append('<div class="materiaHorario materia'+horario.materia_id+' profesor'+horario.username+'">'+horario.nombre+'</div>');
		
		if(celda.children().size() > 1){
			celda.addClass('conflicto');
		}
		
		i++;
		dif--;
	}
	
	
	
}
