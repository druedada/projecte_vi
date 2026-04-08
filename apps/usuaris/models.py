
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

# Relació N:M entre usuaris i adreca
User.add_to_class('adreces', models.ManyToManyField(Adreces, related_name='usuaris'))
