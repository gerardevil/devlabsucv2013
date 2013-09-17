$(document).ready(function() {
    $("#pg_am").hide()
    $("#agregarHor").remove()

    $( "#id_materia" ).change(function() {
        $("#pg_am").show()
        $("#agregarHor").remove()
        $(".horarios").remove()
        $(".horariosl").remove()
        $(".error_am").remove()
        //$(".agregarMat").prepend('<div id="progressbar"></div>')
        var materia_sel = $("#id_materia option:selected").val()
        if (materia_sel != ""){
            $.ajax({
                url : "/horarios_materia",
                type : "POST",
                dataType: "json",
                data : {
                    mat_sel : materia_sel,
                    csrfmiddlewaretoken:  document.getElementsByName('csrfmiddlewaretoken')[0].value
                },
                success : function(data) {
                    if(data.length > 0){
                        $("#cg").append('<label class="horarios" for="horario1">Horario:</label><select id="horario1" class="horarios" name="horario1">')
                        for (var i = 0;i < data.length;i++){
                            d = data[i]
                            $("#horario1").append('<option value="'+ d.valor+'">'+d.dia_semana+" "+d.hora_inicio+"-"+ d.hora_fin+'</option>')
                        }
                        $("#cg").append('</select>')
                        $("#agregarMat").append('<button type="button" id="agregarHor" onclick=addHorario(data)> + </button></td></tr>')                       
                        $('#cantidad_hor').prop('value',1);
                        $("#enviar_am").prop('disabled',false)
                    }else{
                        $("#agregarMat_mb").append('<div class="alert alert-error error_am"><button type="button" class="close" data-dismiss="alert">&times;</button>La materia seleccionada no posee horarios asignados</div>')
                        $("#enviar_am").prop('disabled',true)
                    }
                    $("#pg_am").hide()
                    //console.log($("html").html())
                },
                error : function(xhr,errmsg,err) {
                    alert(xhr.status + ": " + xhr.responseText);
                }
            });
        }
        else{
            $(".horarios").remove()
            $(".horariosl").remove()
            $("#agregarHor").remove()
            $("#agregarMat_mb").append('<div class="alert alert-error error_am"><button type="button" class="close" data-dismiss="alert">&times;</button>Debe seleccionar una materia</div>')
            $("#pg_am").hide()
        }

    });
    $( "#salir_am" ).click(function() {
        $(".horarios").remove()
        $(".horariosl").remove()
        $("#agregarHor").remove()
        $(".error_am").remove()
        $('#id_materia').prop('selectedIndex',0);
        $('#id_aula').prop('selectedIndex',0);
    });

    
});

function addHorario (data) {
    if(data.length > 0){
        $("#agregarMat").append('<tr><th><label id="horario1" class="horariosl" for="horarios">Horario: </label></th><td><select class="horarios" name="horario1">')
        for (var i = 0;i < data.length;i++){
            d = data[i]
            //alert(d.dia_semana+" "+d.hora_inicio+" "+ d.hora_fin)
            //alert('<option value="'+i+'">'+d.dia_semana+" "+d.hora_inicio+" "+ d.hora_fin+'</option>')
            $(".horarios").append('<option value="'+ d.valor+'">'+d.dia_semana+" "+d.hora_inicio+"-"+ d.hora_fin+'</option>')
        }
        $("#agregarMat").append('</select></td></tr>')
        $('#cantidad_hor').prop('value',1);
        $("#enviar_am").prop('disabled',false)
    }else{
        $("#agregarMat_mb").append('<div class="alert alert-error error_am"><button type="button" class="close" data-dismiss="alert">&times;</button>La materia seleccionada no posee horarios asignados</div>')
        $("#enviar_am").prop('disabled',true)
    }
}
