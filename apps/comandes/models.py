from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from apps.vins.models import Vi


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

