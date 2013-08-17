from principal.models import Aula

class ManagerAula:

	def __init__(self):
		pass

	def listarAulas(self):
		return Aula.objects.all()
