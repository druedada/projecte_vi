from django.shortcuts import render
from django.db.models import Q

from .models import Vi


def home(request):
	# Base queryset: vins actius
	qs = Vi.objects.filter(es_actiu=True)

	# Filtre per stock (per defecte mostrar només stock > 0)
	in_stock = request.GET.get('in_stock', '1')
	if in_stock == '1':
		qs = qs.filter(stock__gt=0)

	# Cerca per nom o descripció
	q = request.GET.get('q', '').strip()
	if q:
		qs = qs.filter(Q(nom__icontains=q) | Q(descripcio__icontains=q))

	# Filtre per tipus
	tipus = request.GET.get('tipus', '')
	if tipus:
		qs = qs.filter(tipus=tipus)

	# Filtre per origen
	origen = request.GET.get('origen', '').strip()
	if origen:
		qs = qs.filter(origen__icontains=origen)

	# Ordenació
	order = request.GET.get('order', 'nom_asc')
	if order == 'preu_asc':
		qs = qs.order_by('preu')
	elif order == 'preu_desc':
		qs = qs.order_by('-preu')
	elif order == 'any_asc':
		qs = qs.order_by('any_collita')
	elif order == 'any_desc':
		qs = qs.order_by('-any_collita')
	else:
		qs = qs.order_by('nom')

	# Opcions per a selects (valors existents a la BBDD)
	tipus_choices = Vi.objects.values_list('tipus', flat=True).distinct()
	origens = Vi.objects.values_list('origen', flat=True).distinct()

	context = {
		'vins': qs,
		'q': q,
		'tipus_selected': tipus,
		'origen_selected': origen,
		'order': order,
		'in_stock': in_stock,
		'tipus_choices': tipus_choices,
		'origens': origens,
	}
	return render(request, 'vins/llista_vins.html', context)
