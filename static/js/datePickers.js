 $(function() {

$("input[id^='id_fecha']").addClass("datepicker");
//$( "#id_fecha_fin" ).addClass("datepicker");
$( ".datepicker" ).datepicker({'format' : 'yyyy-mm-dd'});


 $("input[id^='id_hora']" ).attr( "data-format", "hh:mm:ss" );
 $("input[id^='id_hora']").wrap("<div id='hora' class='input-append hora'/div>");
 $(".hora").append("<span class='add-on'><i data-time-icon='icon-time'></i></span>");


$('.hora').datetimepicker({
    pickDate: false,
	pick12HourFormat: true,   // enables the 12-hour format time picker
});


});