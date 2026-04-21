
from django.db import models
from django.contrib.auth.models import User

class Adreces(models.Model):
	class Meta:
		unique_together = ('cp', 'poblacio', 'carrer', 'numero')
	cp = models.CharField(max_length=10, verbose_name='Codi Postal')
	poblacio = models.CharField(max_length=100, verbose_name='Població')
	carrer = models.CharField(max_length=100, verbose_name='Carrer')
	numero = models.CharField(max_length=10, verbose_name='Número')

	def __str__(self):
		return f"{self.carrer}, {self.numero}, {self.cp} {self.poblacio}"


class UsuariDireccio(models.Model):
	class Meta:
		unique_together = ('user', 'direccio')

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adreces_relacions')
	direccio = models.ForeignKey(Adreces, on_delete=models.CASCADE, related_name='usuaris_relacions')

	def __str__(self):
		return f"{self.user} - {self.direccio}"
