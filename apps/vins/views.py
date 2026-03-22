from django.shortcuts import render

from .models import Vi

# Create your views here.


def home(request):
	vins_disponibles = Vi.objects.filter(stock__gt=0).order_by('nom')
	context = {
		'app_title': 'Vins',
		'vins': vins_disponibles,
	}
	return render(request, 'vins/llista_vins.html', context)
