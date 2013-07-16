# Create your views here.



from django.http import HttpResponse
from django.shortcuts import render_to_response
import os


def inicio(request):
		
	return render_to_response('Home.html')
	#return HttpResponse(os.getcwd())
	
def getRecurso(request, recurso):
		
	return render_to_response(recurso)