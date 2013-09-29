
function toggle(source) { checkboxes = document.getElementsByName(source.name);for(var i=0;i<checkboxes.length;i++) { checkboxes[i].checked = source.checked; }}

function untoggleAllCheck(source){  var allcheckboxes = $( "input:checkbox[name='"+source.name+"']").length;  var allCheckedCheckboxes = $( "input:checkbox[name='"+source.name+"']:checked").length;  var all = $( "input:checkbox[name='"+source.name+"'][value='none']" );    for (var i =0; i< all.length;++i ){   if (all[i].checked){all[i].checked = (allCheckedCheckboxes==allcheckboxes);}else{all[i].checked = (allCheckedCheckboxes==(allcheckboxes-1)); } } }

function isAnyCheckSelected()
{
  var checkboxes = $("input[type=checkbox]:checked").not( "[value='none']" ).map(function() {return $(this).val();});
  if(checkboxes.size())
  {
    $.ajax({
        type: 'GET',
        url: '/getemaillist',
        data: {
          'keys': (checkboxes.toArray()).toString(),
        },
        success: function(emails) {
            var to_temp= document.getElementById('to');
            to_temp.value=emails;
            $('#modalContacto').modal('show');
        },
        error: function(xhr, textStatus, errorThrown) {
            alert('Please report this error: '+errorThrown+xhr.status+xhr.responseText);
        }
    });
  }
}


function getSelectedProfile(id)
{
    $.ajax({
        type: 'GET',
        url: '/getprofileinfo/'+id.toString(),
        dataType: 'json',
        success: function(info) {
            var html='<table class="table table-hover"><tbody>';
            html += '<tr><td><b>Cedula</b></td><td>'+info.usuario_id__username+'</td></tr>';
            html += '<tr><td><b>Nombre y Apellido</b></td><td>'+info.usuario_id__first_name+' '+info.usuario_id__last_name+'</td></tr>'; 
            html += '<tr><td><b>Correo Electronico</b></td><td>'+info.usuario_id__email+'</td></tr>';
            html += '<tr><td><b>Telefonos de Contacto</b></td><td>'+info.telefono_celular+' / '+info.telefono_oficina+" / "+info.telefono_casa+'</td></tr>';
            html += '<tr><td><b>Fecha ingreso</b></td><td>'+info.fecha_ingreso+'</td></tr>';
            html += '<tr><td><b>Direccion</b></td><td>'+info.direccion+'</td></tr>';
            html += '<tr><td><b>Tipo contrato</b></td><td>'+info.tipo_contrato__nombre+'</td></tr>';
            html += '<tr><td><b>Dedicacion</b></td><td>'+info.dedicacion+'</td></tr>';
            if (info.estatus == 'A')
              html += '<tr><td><b>Estatus</b></td><td>Activo(a)</td></tr></tbody></table>';
            else if (info.estatus == 'I')
              html += '<tr><td><b>Estatus</b></td><td>Inactivo(a)</td></tr></tbody></table>';

            $('#modalPerfil .modal-body').html(html); 
            $('#modalPerfil .modal-body table tr').css("background-color", "#E6EDF9"); 
            $('#modalPerfil').modal('show');
        },
        error: function(xhr, textStatus, errorThrown) {
            alert('Please report this error: '+errorThrown+xhr.status+xhr.responseText);
        }
    });
}

