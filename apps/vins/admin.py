from django.contrib import admin

from .models import Vi


@admin.register(Vi)
class ViAdmin(admin.ModelAdmin):
	list_display = ('nom', 'tipus', 'preu', 'stock', 'any_collita')
	list_filter = ('tipus',)
	search_fields = ('nom', 'descripcio')
