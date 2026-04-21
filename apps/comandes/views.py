from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.comandes.models import Carret
from apps.vins.models import Vi

# Create your views here.

@login_required
def carret(request):
	carret_items = request.user.carret_items.select_related('vi')
	total = sum(item.vi.preu * item.unitats for item in carret_items)

	# La plantilla usa los nombres cart_items / quantitat / subtotal.
	cart_items = []
	for item in carret_items:
		subtotal = item.vi.preu * item.unitats
		cart_items.append({
			'vi': item.vi,
			'quantitat': item.unitats,
			'subtotal': subtotal,
		})

	return render(request, 'comandes/carret.html', {'cart_items': cart_items, 'total': total})


def afegir_al_carret(request, vi_id):
	if request.method != 'POST':
		return redirect('llista_vins')

	if not request.user.is_authenticated:
		return redirect('usuaris:registre')

	vi = get_object_or_404(Vi, id=vi_id, es_actiu=True)

	try:
		quantitat = int(request.POST.get('quantitat', 1))
	except (TypeError, ValueError):
		quantitat = 1

	quantitat = max(1, quantitat)
	quantitat = min(quantitat, vi.stock)

	if quantitat <= 0:
		return redirect('llista_vins')

	carret_item, created = request.user.carret_items.get_or_create(vi=vi)
	if created:
		carret_item.unitats = quantitat
	else:
		carret_item.unitats = min(carret_item.unitats + quantitat, vi.stock)

	carret_item.save()
	messages.success(request, f"{vi.nom} s'ha afegit al carret.")
	return redirect('llista_vins')

@login_required
def eliminar_del_carret(request, vi_id):
	if request.method != 'POST':
		return redirect('comandes:carret')

	item = get_object_or_404(Carret, user=request.user, vi_id=vi_id)
	item.delete()
	return redirect('comandes:carret')

@login_required
def actualitzar_quantitat(request, vi_id):
	if request.method != 'POST':
		return redirect('comandes:carret')

	item = get_object_or_404(Carret.objects.select_related('vi'), user=request.user, vi_id=vi_id)
	action = request.POST.get('action')

	if action == 'inc':
		nova_quantitat = item.unitats + 1
	elif action == 'dec':
		nova_quantitat = item.unitats - 1
	else:
		try:
			nova_quantitat = int(request.POST.get('quantitat', item.unitats))
		except (TypeError, ValueError):
			nova_quantitat = item.unitats

	if nova_quantitat <= 0:
		item.delete()
		return redirect('comandes:carret')

	item.unitats = min(nova_quantitat, item.vi.stock)
	item.save()
	return redirect('comandes:carret')
