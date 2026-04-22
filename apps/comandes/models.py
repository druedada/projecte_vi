from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from apps.vins.models import Vi
from apps.usuaris.models import Adreces


class Carret(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carret_items')
	vi = models.ForeignKey(Vi, on_delete=models.CASCADE, related_name='carret_items')
	unitats = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
	
	class Meta:
		unique_together = ('user', 'vi')
		verbose_name = 'Item del carret'
		verbose_name_plural = 'Items del carret'

	def __str__(self):
		return f"{self.user.username} - {self.vi.nom} ({self.unitats})"


class Comanda(models.Model):
	"""Representa una comanda realitzada per un usuari a partir del seu carret."""

	class Estat(models.TextChoices):
		PENDENT = 'PENDENT', 'Pendent'
		CONFIRMADA = 'CONFIRMADA', 'Confirmada'
		ENVIADA = 'ENVIADA', 'Enviada'
		ENTREGADA = 'ENTREGADA', 'Entregada'
		CANCELLADA = 'CANCELLADA', 'Cancel·lada'

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comandes')
	direccio = models.ForeignKey(Adreces, on_delete=models.SET_NULL, null=True, related_name='comandes')
	estat = models.CharField(max_length=12, choices=Estat.choices, default=Estat.PENDENT)
	data_creacio = models.DateTimeField(auto_now_add=True)
	data_actualitzacio = models.DateTimeField(auto_now=True)
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

	class Meta:
		ordering = ['-data_creacio']
		verbose_name = 'Comanda'
		verbose_name_plural = 'Comandes'

	def __str__(self):
		return f"Comanda #{self.pk} - {self.user.username} ({self.get_estat_display()})"

	def calcular_total(self):
		"""Recalcula el total a partir de les línies de la comanda."""
		self.total = sum(linia.subtotal for linia in self.linies.all())
		self.save(update_fields=['total'])


class LineaComanda(models.Model):
	"""Cada línia representa un vi comprat dins d'una comanda, amb el preu fixat al moment de la compra."""

	comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name='linies')
	vi = models.ForeignKey(Vi, on_delete=models.SET_NULL, null=True, related_name='linies_comanda')
	unitats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
	preu_unitari = models.DecimalField(max_digits=8, decimal_places=2)

	class Meta:
		verbose_name = 'Línia de comanda'
		verbose_name_plural = 'Línies de comanda'

	@property
	def subtotal(self):
		"""Retorna el subtotal de la línia (preu_unitari × unitats)."""
		return self.preu_unitari * self.unitats

	def __str__(self):
		nom_vi = self.vi.nom if self.vi else 'Vi eliminat'
		return f"{nom_vi} x{self.unitats} @ {self.preu_unitari}€"
