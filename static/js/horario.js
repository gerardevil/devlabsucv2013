
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
	$('#tablaProfesores').showLoading({'indicatorZIndex' : 101,'overlayZIndex': 100});

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

							var status = 'P'

							if ( ~$('#rol_usuario').text().indexOf('Coordinador(a)') )
							{
								status = 'AC';
							}else if (~$('#rol_usuario').text().indexOf('Jefe(a) de Departamento'))
							{
								status = 'AJ';
							}
							$(this).data('estatus',status);
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

							var status = 'P'

							if ( ~$('#rol_usuario').text().indexOf('Coordinador(a)') )
							{
								status = 'RC';
							}else if (~$('#rol_usuario').text().indexOf('Jefe(a) de Departamento'))
							{
								status = 'RJ';
							}
							$(this).data('estatus',status);


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
	$('#tablaMaterias').showLoading({'indicatorZIndex' : 101,'overlayZIndex': 100});

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
		html = '<div id="materia'+idMateriaHorario+'" class="materiaHorario">';

		if(horario.estatus == 'AC' || horario.estatus == 'AJ'){
			html += '<i class="icono icon-ok pull-right" style="color:green;"></i>';
		}else if(horario.estatus == 'RC' || horario.estatus == 'RJ'){
			html += '<i class="icono icon-remove pull-right" style="color:red;"></i>';
		}else if(horario.estatus == 'PJ' || horario.estatus == 'P'){
			html += '<i class="icono icon-time pull-right" style="color:#000000;"></i>';
		}else{
			html += '<i class="icono icon-question-sign"></i>';}

		if(horario.incompleto == 'I')
			html += '<i class="icon-warning-sign pull-left" style="color:#F45000;" data-toggle="tooltip" title="Envio Incompleto de '+horario.centro+'"></i>';

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
		html += '<h5>Estatus</h5>' + horario.descripcion_estatus;
		
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

	if ( ~$('#rol_usuario').text().indexOf('Coordinador(a)') )
	{
		datos["rol"]='cc';
	}
	
	$('#tablaHorario').hideLoading();
	$('#tablaHorario').showLoading({'indicatorZIndex' : 101,'overlayZIndex': 100});
	
	param = 'data='+JSON.stringify(datos);
	
	//alert(param);
	
	$.ajax({  
		 type: 'POST',  
		 url: '/changestatus',
		 data: param,
		 success: function(res){

		 	cargarHorario();	
		 	
		 	var text = '<b>Horario de solicitudes guardado satisfactoriamente</b></br></br>'
		 	var html = '<div class="alert alert-success" style="width:80%" >';

		 	if(parseInt(res,10) > 0 )
		 	{
		 		html = '<div class="alert" style="width:80%" >';
		 		text +=  '<b>Nota: </b>El sistema ha detectado que (  '+res+'  ) profesores aun no han enviado su solicitud'
		 	}

			html += '<button type="button" class="close" data-dismiss="alert">&times;</button>';
			html += (text+'</div>');
			
			$('#saveButton').parent().prepend(html);		
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

	
	if ( ~$('#rol_usuario').text().indexOf('Coordinador(a)') )
	{
		datos["rol"]='cc';
	}

	$('#tablaHorario').hideLoading();
	$('#tablaHorario').showLoading({'indicatorZIndex' : 101,'overlayZIndex': 100});
	
	param = 'data='+JSON.stringify(datos);
	
	//alert(param);
	
	$.ajax({  
		 type: 'POST',  
		 url: '/changestatus',
		 data: param,
		 success: function(res){		 	

		 	cargarHorario();

		 	var text = '<b>Horario de solicitudes enviado al Jefe de Departamento</b></br></br>'
		 	var html = '<div class="alert alert-success" style="width:80%" >';

		 	if(parseInt(res,10) > 0 )
		 	{
		 		html = '<div class="alert" style="width:80%" >';
		 		text +=  '<b>Nota: </b>El sistema ha detectado que (  '+res+'  ) profesores aun no han enviado su solicitud'
		 	}

			html += '<button type="button" class="close" data-dismiss="alert">&times;</button>';
			html += (text+'</div>');
			
			$('#saveButton').parent().prepend(html);
		 },
		 complete: function(){
			$('#tablaHorario').hideLoading();
		 },
		 error: function(xhr,errmsg,err){
			console.error(xhr.status + ": " + xhr.responseText);
		 }
		});
}

$( "#chartButton" ).click(function(event) {	
	$.ajax({
	    type: 'POST',
	    url: '/chart',
	    datatype: "json",
	    success: function(respuesta){
	    	var labelsA = new Array();
	    	var remainingCountersA = new Array();
	    	var actives = new Array();
	    	var inactives = new Array();
	    	var max = -1;
	    	//aux2.push($(this).data('solicitud'));
	    	for(var i=0;i<respuesta.length;++i){
				labelsA.push(respuesta[i].name);
				remainingCountersA.push(respuesta[i].remaining);
				actives.push(respuesta[i].actives);
				inactives.push(respuesta[i].inactives);
			}
			var getMax ={max : function( array ){return Math.max.apply( Math, array ); } }
			max = getMax.max([ getMax.max(remainingCountersA),getMax.max(actives),getMax.max(inactives)])
			
			console.log(remainingCountersA)
			console.log(actives)
			console.log(inactives)
			
			var ctx = document.getElementById("ppxc").getContext("2d");
			var data = {
							labels : labelsA,
							datasets : 
							[
								{
									fillColor : "#97E1DF",
									strokeColor : "#FFFFFF",
									data : inactives
								},
								{
									fillColor : "#79BEF7",
									strokeColor : "#FFFFFF",
									data : actives
								},
								{
									fillColor : "#5460F5",
									strokeColor : "#FFFFFF",
									data : remainingCountersA
								},
							]
						}
			var opt = {
					scaleFontSize : 12,	
					barValueSpacing : 2,
					scaleOverride : true,
					scaleSteps : max,
					scaleStepWidth : 1,
					scaleStartValue : 0,
					scaleGridLineColor : "#C9CBD1",
					scaleGridLineWidth : 1,	
				}
			new Chart(ctx).Bar(data,opt);
			$("#incompleteCharts").modal('show');
	    },
	    error: function(xhr, textStatus, errorThrown) {
	    	alert("Error : "+errorThrown+"\nStatus:"+textStatus+"\nxhr:"+xhr);
	    }
    });    
});