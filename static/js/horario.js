
$(function(){

	$('#tablaProfesores tbody').html('<tr><td>Cargando...</td></tr>');
	$('#tablaMaterias tbody').html('<tr><td>Cargando...</td></tr>');
	cargarHorario();
	cargarProfesores();
	cargarMaterias();

});



function cargarHorario(){

	$('#tablaHorario').hideLoading();
	$('#tablaHorario').showLoading();
	
	var url = '/schedulexrequest/cc';
	var param = '';
	
	$.ajax({  
		 type: 'GET',  
		 url: url,
		 dataType: 'json',
		 //data: param,
		 success: function(respuesta){
			for(i=0;i<respuesta.length;i++){
			
				insertarMateriaHorario(respuesta[i]);
				
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
				html += '<button type="submit" class="btn btn-mini" style="margin-left:5px;float:right;">';
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
				html += '<button type="submit" class="btn btn-mini" style="margin-left:5px;float:right;">';
				html += '	<i class="icon-eye-open"></i>';
				html += '</button></td></tr>';
				
			}
			
			if(respuesta.length = 0){
				html += '<tr><td>No hay materias propuestas</td></tr>';
			}
			
			$('#tablaMaterias tbody').html(html);
			
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

	horario.fecha_inicia;

}
