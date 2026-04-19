from django.contrib import admin
from .models import Carret


@admin.register(Carret)
class CarretAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'vi', 'unitats')
	search_fields = ('user__username', 'vi__nom')
