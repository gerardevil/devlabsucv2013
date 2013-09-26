function Mostrar_modal_eliminar(object)
{
  var botonEliminar = document.getElementById('eliminar_obj');
  botonEliminar.setAttribute("href",object.id);
  var html= '';
  html+='<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>';
  html+='<h4>Borrar <b style="color:#4380D3;">'+object.name+'</b> </h4>';  
  $('#modalEliminarHeader').html(html);
  $('#modal_eliminar').modal('show');
}

