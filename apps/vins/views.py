from django.shortcuts import render

from .models import Vi

# Create your views here.


def home(request):
	# Mostra els vins disponibles (stock > 0) i actius ordenats alfabèticament per nom
	vins_disponibles = Vi.objects.filter(stock__gt=0, es_actiu=True).order_by('nom')
	context = {
		'vins': vins_disponibles,
	}
	return render(request, 'vins/llista_vins.html', context)
