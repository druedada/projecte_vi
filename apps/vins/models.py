from django.db import models


class Vi(models.Model):
	class Tipus(models.TextChoices):
		BLANC = 'BLANC', 'Blanc'
		NEGRE = 'NEGRE', 'Negre'
		ROSAT = 'ROSAT', 'Rosat'
		ESPUMOS = 'ESPUMOS', 'Espumos'

	nom = models.CharField(max_length=150)
	origen = models.CharField(max_length=120, blank=True, default='')
	tipus = models.CharField(max_length=10, choices=Tipus.choices)
	preu = models.DecimalField(max_digits=8, decimal_places=2)
	stock = models.IntegerField(default=0)
	any_collita = models.IntegerField()
	imatge = models.ImageField(upload_to='vins/', blank=True, null=True)
	descripcio = models.TextField()

	class Meta: # Django  pluralitza aplicant una "s" al final, però en aquest cas el plural de "Vi" és "Vins", no "Vis"
		verbose_name = "Vi"
		verbose_name_plural = "Vins"

	def __str__(self):
		return self.nom
