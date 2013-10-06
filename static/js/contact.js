$( "#contactSubmitButton" ).click(function(event) {	
	event.preventDefault();
	$.ajax({
        type: 'POST',
        url: '/contact',
        datatype: "json",        
        data: {
          'to': $("#modalContacto .modal-body #emailForm #to").val(),
          'matter': $("#modalContacto .modal-body #emailForm #matter").val(),
          'message':$("#modalContacto .modal-body #emailForm #content").val(),
        },
        success: function(respuesta){
        	var html ='Notificaciones enviadas satisfactoriamente.';
        	$("#modalOK .modal-body #okText").html(html);
        	$("#modalOK").modal('show');
        },
        error: function(xhr, textStatus, errorThrown) {
        	alert("Error : "+errorThrown+"\nStatus:"+textStatus+"\nxhr:"+xhr);
        }
    });
    $("#modalContacto").modal('hide');
});