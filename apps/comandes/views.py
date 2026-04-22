from urllib import request

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.comandes.models import Carret, Comanda, LineaComanda
from apps.usuaris.models import UsuariDireccio
from apps.usuaris.forms import AdressForm
from apps.vins.models import Vi


# Create your views here.

@login_required
def _build_cart_context(request):
	"""Construeix el context comú del carret per a les vistes."""
	carret_items = request.user.carret_items.select_related('vi')
	total = sum(item.vi.preu * item.unitats for item in carret_items)

	cart_items = []
	for item in carret_items:
		subtotal = item.vi.preu * item.unitats
		cart_items.append({
			'vi': item.vi,
			'quantitat': item.unitats,
			'subtotal': subtotal,
		})

	return {'cart_items': cart_items, 'total': total}


@login_required
def carret(request):
	context = _build_cart_context(request)
	return render(request, 'comandes/carret.html', context)

@login_required
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
	return redirect(request.POST.get('next', 'llista_vins')) 

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


@login_required
def confirmar_comanda(request):
	"""
	Flux de confirmació de comanda:
	1. Si el carret està buit → redirigeix al carret.
	2. Si l'usuari NO té cap adreça → mostra el formulari d'adreça dins la pàgina del carret.
	3. Un cop l'usuari té adreça → crea la Comanda + LineaComanda, descompta stock i buida el carret.
	"""
	if request.method != 'POST':
		return redirect('comandes:carret')

	carret_items = request.user.carret_items.select_related('vi')
	if not carret_items.exists():
		messages.warning(request, "El carret està buit.")
		return redirect('comandes:carret')

	# Comprovar si l'usuari té alguna adreça vinculada
	relacio_direccio = UsuariDireccio.objects.filter(user=request.user).select_related('direccio').first()

	if not relacio_direccio:
		# L'usuari no té adreça → mostrar el formulari d'adreça
		# Si ens arriba amb dades del formulari d'adreça (camp 'cp' present), intentem guardar-lo
		if 'cp' in request.POST:
			form = AdressForm(request.POST)
			if form.is_valid():
				form.save(user=request.user)
				messages.success(request, "Adreça guardada correctament. Confirma la comanda.")
				# Redirigir de nou al carret perquè ara ja té adreça i pot confirmar
				context = _build_cart_context(request)
				context['mostrar_confirmacio'] = True
				return render(request, 'comandes/carret.html', context)
		else:
			form = AdressForm()

		# Renderitzar el carret amb el formulari d'adreça visible
		context = _build_cart_context(request)
		context['mostrar_form_direccio'] = True
		context['form_direccio'] = form
		return render(request, 'comandes/carret.html', context)

	# L'usuari ja té adreça → procedir a crear la comanda
	direccio = relacio_direccio.direccio

	with transaction.atomic():
		# Crear la comanda
		comanda = Comanda.objects.create(
			user=request.user,
			direccio=direccio,
			estat=Comanda.Estat.PENDENT,
			total=0,
		)

		total = 0
		for item in carret_items:
			# Comprovar stock disponible
			if item.vi.stock < item.unitats:
				messages.error(request, f"No hi ha prou stock de {item.vi.nom}. Disponible: {item.vi.stock}.")
				comanda.delete()
				return redirect('comandes:carret')

			subtotal = item.vi.preu * item.unitats
			total += subtotal

			LineaComanda.objects.create(
				comanda=comanda,
				vi=item.vi,
				unitats=item.unitats,
				preu_unitari=item.vi.preu,
			)

			# Descomptar stock
			item.vi.stock -= item.unitats
			item.vi.save(update_fields=['stock'])

		# Actualitzar el total de la comanda
		comanda.total = total
		comanda.save(update_fields=['total'])

		# Buidar el carret de l'usuari
		request.user.carret_items.all().delete()

	messages.success(request, f"Comanda #{comanda.pk} creada correctament! Total: {comanda.total:.2f} €")
	return redirect('comandes:carret')
