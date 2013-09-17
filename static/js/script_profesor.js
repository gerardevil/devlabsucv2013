$(document).ready(function() {
    $("#pg_am").hide()
    $("#agregarHor").remove()
    //var i = $('#agregarMat_mb select.horarios').size() + 2;

    $( "#id_materia" ).change(function() {
        $("#pg_am").show()
        $("#agregarHor").remove()
        $(".horarios").remove()
        $(".horariosl").remove()
        $(".error_am").remove()
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
                        $("#cg").append('<button type="button" id="agregarHor" > + </button>')                       
                        $('#cantidad_hor').attr('value',1);
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
            $('#cantidad_hor').attr('value',0);
        }

    });
    $( "#salir_am" ).click(function() {
        $(".horarios").remove()
        $(".horariosl").remove()
        $("#agregarHor").remove()
        $(".error_am").remove()
        $('#id_materia').prop('selectedIndex',0);
        $('#id_aula').prop('selectedIndex',0);
        $('#cantidad_hor').attr('value',0);
    });

    $('#agregarHor').live('click' , function() {
        var i = $('#cantidad_hor').attr('value')
        i++
        ch = parseInt(i)
        $('#horario1').clone().attr('id', 'horario'+i).attr('name', 'horario'+i).appendTo('#cg');
        $('#horario'+i).append('<button type="button" id="eliminarHor" > - </button>'); // selecionar el combobox recien a;adido y agregar boton -
        $('#cantidad_hor').attr('value',ch);
        //i++;
        //console.log($('#cantidad_hor').attr('value'))
    });

    $('#eliminarHor').live('click' , function() {
        if (i > 2){
        $(this).parents('.horarios').remove(); //elimminar el combobox
        $(this).parents('#horario'+i).remove();

        //i--;
        }
    });
});

