function toggle(source) {
  checkboxes = document.getElementsByName(source.name);
  for(var i=0;i<checkboxes.length;i++) {
    checkboxes[i].checked = source.checked;
  }
}

function isAnyCheckSelected(source)
{
  var checkboxes = $("input[type=checkbox]:checked");
  if(checkboxes.size())
  {
    to="";
    for(var i =0; i< checkboxes.size();++i)
    {
      if(checkboxes[i].value!="none"){
        to+=checkboxes[i].value+";"
      }
    }
    to_temp= document.getElementById('to');
    to_temp.value=to;
    $('#modalContacto').modal('show');
  }
}

