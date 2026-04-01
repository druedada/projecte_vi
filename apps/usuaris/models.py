
from django.db import models
from django.contrib.auth.models import User

class Adreces(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='adreca')
	cp = models.CharField(max_length=10, verbose_name='Codi Postal')
	poblacio = models.CharField(max_length=100, verbose_name='Població')
	carrer = models.CharField(max_length=100, verbose_name='Carrer')
	numero = models.CharField(max_length=10, verbose_name='Número')

	def __str__(self):
		return f"{self.carrer}, {self.numero}, {self.cp} {self.poblacio}"
