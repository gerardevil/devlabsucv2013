function toggle(source) {
  checkboxes = document.getElementsByName(source.name);
  for(var i=0;i<checkboxes.length;i++) {
    checkboxes[i].checked = source.checked;
  }
}

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

