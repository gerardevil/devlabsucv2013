$(document).ready(function() {
    $("#pg_am").hide()
    $("#agregarHor").hide()

    $( "#id_materia" ).change(function() {
        $("#pg_am").show()
        $(".horarios").remove()
        $(".horariosl").remove()
        $(".error_am").remove()
        $(".eliminarHor").remove()
        $("#agregarHor").hide()
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
                        $("#cg").append('</select><br>')
                        $('#cantidad_hor').attr('value',1)
                        $("#enviar_am").prop('disabled',false)
                        $("#agregarHor").show()
                    }else{
                        $("#agregarMat").append('<div class="alert alert-error error_am"><button type="button" class="close" data-dismiss="alert">&times;</button>La materia seleccionada no posee horarios asignados</div>')
                        $("#enviar_am").prop('disabled',true)
                        $("#agregarHor").hide()
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
            $("#agregarMat").append('<div class="alert alert-error error_am"><button type="button" class="close" data-dismiss="alert">&times;</button>Debe seleccionar una materia</div>')
            $("#pg_am").hide()
            $('#cantidad_hor').attr('value',0);
        }

    });

    $( "#salir_am" ).click(function() {
        $(".horarios").remove()
        $(".horariosl").remove()
        $(".error_am").remove()
        $('#id_materia').prop('selectedIndex',0);
        $('#id_aula').prop('selectedIndex',0);
        $('#cantidad_hor').attr('value',0);
        $("#agregarHor").hide()
        $(".eliminarHor").remove()
        $('.agregarMateria br').remove()
    });

    $('#agregarHor').live('click' , function() {
        var i = $('#cantidad_hor').attr('value')
        i++
        var ch = parseInt(i)
        $('#horario1').clone().attr('id', 'horario'+i).attr('name', 'horario'+i).appendTo('#cg')
        $('#cg').append('<a class="btn btn-mini eliminarHor"><i class="icon-remove"></i></a><br>') // selecionar el combobox recien a;adido y agregar boton -
        $('#cantidad_hor').attr('value',ch);
        //console.log($('#cantidad_hor').attr('value'))
    });

    $('.eliminarHor').live('click' , function() {
        $(this).prev().prev().remove()
        $(this).prev().remove()
        $(this).remove()
        var i = $('#cantidad_hor').attr('value')
        i--
        var ch = parseInt(i)
        $('#cantidad_hor').attr('value',ch);
        //console.log($('#cantidad_hor').attr('value'))
    });

    $('.bot_borrar').live('click',function() {
        var valor = $(this).attr('value')
        //console.log("Hola "+valor)
        $("#bborrar").attr("href","/propuesta/borrar/"+valor)

    });

    $( "#salirE_am" ).click(function() {
        $('#agregarMatE select').prop('selectedIndex',0);
        $('#agregarMatE input').attr('value',"");
        $("#enviarE_am").prop('disabled',true)
    });

    function activarBoton(){
        si1 = $("#agregarMateriaE #id_materia").prop('selectedIndex')
        si2 = $("#agregarMateriaE #id_aula").prop('selectedIndex')
        it1 = $("#agregarMateriaE #id_hora_inicio").val()
        it2 = $("#agregarMateriaE #id_hora_fin").val()
        if((si1 != 0) && (si2 != 0) && (it1 != '') && (it2 != '')){
            $("#enviarE_am").prop('disabled',false)
        }else{
            $("#enviarE_am").prop('disabled',true)
        }
    }

    $("#agregarMateriaE select").change(function(){
            activarBoton()
    });

    $("#agregarMateriaE input").keyup(function(){
            activarBoton()
    });
});

