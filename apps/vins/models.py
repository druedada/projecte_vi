from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Constants globals per a validar l'any de collita dels vins
MIN_ANY_COLLITA = 1800
MAX_ANY_COLLITA = datetime.date.today().year

#! Despres de fer modificacións:
# 1. Fer migracions a BBDD: python manage.py makemigrations
# 2. Aplicar migracions a BBDD: python manage.py migrate

#? Estructura de la bbdd per a vins:
class Vi(models.Model):  
	class Tipus(models.TextChoices): # Enum per a tipus de vi
		#Constant python = Valor BBDD , Valor llegible per a l'usuari
		BLANC = 'BLANC', 'Blanc'
		NEGRE = 'NEGRE', 'Negre'
		ROSAT = 'ROSAT', 'Rosat'
		ESPUMOS = 'ESPUMOS', 'Espumos'
    #? Camps de la taula Vi:
	nom = models.CharField(max_length=150)
	origen = models.CharField(max_length=120)
	tipus = models.CharField(max_length=10, choices=Tipus.choices) # El camp tipus té els valors definits a la class Tipus
	preu = models.DecimalField(max_digits=8, decimal_places=2)
	stock = models.IntegerField(default=0)
	any_collita = models.IntegerField(
	    validators=[ # Validació per a assegurar que l'any de collita està dins dels límits definits per les constants
	        MinValueValidator(MIN_ANY_COLLITA),
	        MaxValueValidator(MAX_ANY_COLLITA)
	    ]
	)
	imatge = models.ImageField(upload_to='vins/', blank=True, null=True)
	descripcio = models.TextField() # Camp de text llarg per a la descripció del vi


	def __str__(self): # Retorna el nom del vi quan es mostra com a string (per exemple, al panell d'administració)
		return self.nom
	class Meta: # Django  pluralitza aplicant una "s" al final, però en aquest cas el plural de "Vi" és "Vins", no "Vis"
		verbose_name = "Vi"
		verbose_name_plural = "Vins"

	def save(self, *args, **kwargs):  
		old_image_name = None #Variable per a guardar el nom de l'imatge

		if self.pk: # Si l'objecte ja existeix (té una clau primària), obtenim el nom de l'imatge antiga abans de guardar els canvis
			old_image_name = type(self).objects.filter(pk=self.pk).values_list('imatge', flat=True).first()

		super().save(*args, **kwargs) 
		# Si hi havia una imatge antiga i el nom de la nova imatge és diferent, eliminem l'imatge antiga del sistema de fitxers
		new_image_name = self.imatge.name if self.imatge else None 
		if old_image_name and old_image_name != new_image_name:
			self.imatge.storage.delete(old_image_name)
