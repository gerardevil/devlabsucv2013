
$(function(){

	cargarHorario();
	//cargarProfesores();
	//cargarMaterias();
	$(".nano").nanoScroller();
	$(".submenu").addClass("hidden");
	$(".pane").css("display","block");
	$(".slider").css("display","block");

});



function cargarHorario(){

	$('#tablaHorario').hideLoading();
	$('#tablaHorario').showLoading();
	
	var url = '/prueba/cc';
	var param = '';
	
	$.ajax({  
		 type: 'GET',  
		 url: url,
		 dataType: 'json',
		 data: param,
		 success: function(respuesta){
			alert(respuesta);
			alert(respuesta.length);
			for(i=0;i<respuesta.length;i++){
			
				alert(respuesta[i+'']['nombre']);
				
			}
			
		 },
		 complete: function(){
			$('#tablaHorario').hideLoading();
		 },
		 error: function(err,errmsg){
			alert(errmsg);
		 }
		});
}

function cargarProfesores(){

	$('#tablaProfesores').hideLoading();
	$('#tablaProfesores').showLoading();
	
	var url = '';
	var param = '';
	
	$.ajax({  
		 type: 'GET',  
		 url: url,
		 dataType: 'json',
		 data: param,
		 success: function(respuesta){
			
		 },
		 complete: function(){
			$('#tablaProfesores').hideLoading();
		 }
		});

}

function cargarMaterias(){

	$('#tablaMaterias').hideLoading();
	$('#tablaMaterias').showLoading();
	
	var url = '';
	var param = '';
	
	$.ajax({  
		 type: 'GET',  
		 url: url,
		 dataType: 'json',
		 data: param,
		 success: function(respuesta){
			
		 },
		 complete: function(){
			$('#tablaMaterias').hideLoading();
		 }
		});

}