$( "form" ).submit(function() {	var pass = $("input:password").map(function(){return this.value;});	var i;	for(i=0;i<pass.length;++i)	{		if(pass[i]==""){break;}	}if(i==pass.length)	{return true;}else{$('#alertErrorDiv').html('<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">&times;</button><h4>¡Error!</h4>Ninguna de las Contaseñas puede estar vacias.</div>');return false;}});