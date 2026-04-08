from django.contrib import admin
from .models import Vi

# Model Vi per al admin site de Django amb personalització de les columnes que es mostren, filtres i camp de cerca.
@admin.register(Vi)
class ViAdmin(admin.ModelAdmin):
	list_display = ('nom', 'tipus', 'preu', 'stock', 'any_collita')
	list_filter = ('tipus',)
	search_fields = ('nom', 'tipus', 'any_collita')
