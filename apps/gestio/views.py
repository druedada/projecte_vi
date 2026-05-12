from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count, Sum, Avg, Min, Max, Q
from urllib.parse import urlencode
from django.urls import reverse
from axes.handlers.proxy import AxesProxyHandler
from apps.vins.models import Vi
from django.contrib.auth.models import User
from apps.comandes.models import Carret, Comanda, LineaComanda
from .forms import ViForm


@login_required # Només usuaris autenticats poden accedir
@permission_required('vins.view_vi') # Només usuaris amb el permís de visualitzar vins poden accedir
def vins(request):   
	qs = Vi.objects.all()

	# Cerca simple
	q = request.GET.get('q', '').strip()
	if q:
		qs = qs.filter(Q(nom__icontains=q) | Q(descripcio__icontains=q))

	# Filtre per tipus i origen
	tipus = request.GET.get('tipus', '')
	if tipus:
		qs = qs.filter(tipus=tipus)

	origen = request.GET.get('origen', '').strip()
	if origen:
		qs = qs.filter(origen__icontains=origen)

	# Filtre per estat actiu/inactiu (si s'especifica)
	estat = request.GET.get('estat', '')
	if estat == 'actiu':
		qs = qs.filter(es_actiu=True)
	elif estat == 'inactiu':
		qs = qs.filter(es_actiu=False)

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

	tipus_choices = Vi.objects.values_list('tipus', flat=True).distinct()
	origens = Vi.objects.values_list('origen', flat=True).distinct()

	context = { # Context que es passarà al template per a renderitzar la pàgina del dashboard
		'app_title': 'Gestió de vins',
		'vins': qs,
		'q': q,
		'tipus_choices': tipus_choices,
		'origens': origens,
		'tipus_selected': tipus,
		'origen_selected': origen,
		'order': order,
	}
	return render(request, 'gestio/vins/gestio_vins.html', context)


@login_required
@permission_required('vins.add_vi')
def crear_vi(request): 
	if request.method == 'POST': # Si l'usuari ha enviat el formulari de creació de vi
		form = ViForm(request.POST, request.FILES) # Crea un objecte de formulari amb les dades enviades per l'usuari (tant dades del formulari com fitxers, com la imatge del vi)
		if form.is_valid(): # Si el formulari és vàlid després de la validació
			form.save()
			return redirect('gestio:vins')
	else:
		form = ViForm() 

	context = {
		'app_title': 'Crear vi',
		'form': form,
		'submit_text': 'Crear',
	}
	return render(request, 'gestio/vins/form.html', context)


@login_required
@permission_required('vins.change_vi')
def editar_vi(request, vi_id): 
	vi = get_object_or_404(Vi, pk=vi_id) # Obtenim el vi que volem editar a partir de la seva clau primària (ID). Si no existeix, retornem un error 404.
	if request.method == 'POST': # Si l'usuari ha enviat el formulari d'edició de vi
		form = ViForm(request.POST, request.FILES, instance=vi) # Crea un objecte de formulari amb les dades enviades per l'usuari 
		if form.is_valid():
			form.save()
			return redirect('gestio:vins')
	else:
		form = ViForm(instance=vi)

	context = {
		'app_title': f'Editar: {vi.nom}',
		'form': form,
		'vi': vi,
		'submit_text': 'Guardar canvis',
	}
	return render(request, 'gestio/vins/form.html', context)


@login_required
@permission_required('vins.delete_vi')
def eliminar_vi(request, vi_id):
	vi = get_object_or_404(Vi, pk=vi_id)
	if request.method == 'POST':
		vi.delete() # Elimina el vi de la base de dades
		return redirect('gestio:vins')
	return redirect('gestio:vins')

@login_required
@permission_required('vins.change_vi')
def activar_desactivar_vi(request, vi_id):
	vi = get_object_or_404(Vi, pk=vi_id)
	vi.es_actiu = not vi.es_actiu # Canvia l'estat d'actiu a l'invers del que és actualment
	vi.save() # Guarda els canvis a la base de dades
	return redirect('gestio:vins')

@login_required
@permission_required('vins.view_vi')
def estadistiques_redirect(request):
	return redirect('gestio:estadistiques_vins')


@login_required
@permission_required('vins.view_vi')
def estadistiques_vins(request):
	return _estadistiques(request, 'vins')


@login_required
@permission_required('vins.view_vi')
def estadistiques_vendes(request):
	return _estadistiques(request, 'vendes')


@login_required
@permission_required('vins.view_vi')
def estadistiques_usuaris(request):
	return _estadistiques(request, 'usuaris')


def _estadistiques(request, section):
	can_manage_orders = (
		request.user.is_staff
		or request.user.is_superuser
		or request.user.groups.filter(name='Gestor').exists()
		or request.user.has_perm('comandes.change_comanda')
	)
	can_manage_users = (
		request.user.is_staff
		or request.user.is_superuser
		or request.user.groups.filter(name='Gestor').exists()
		or request.user.has_perm('auth.change_user')
	)
	users_q = request.POST.get('q', request.GET.get('q', '')).strip()

	if section == 'usuaris' and request.method == 'POST':
		if not can_manage_users:
			messages.error(request, 'No tens permisos per gestionar comptes d\'usuari.')
			return redirect(f'gestio:estadistiques_{section}')

		user_id = request.POST.get('user_id')
		action = request.POST.get('user_action')
		user_obj = get_object_or_404(User, pk=user_id)

		if action == 'toggle_active': # Bloqueja o desbloqueja l'usuari al model User 
			user_obj.is_active = not user_obj.is_active
			user_obj.save(update_fields=['is_active'])
			message = 'Compte activat.' if user_obj.is_active else 'Compte bloquejat.'
			messages.success(request, f'Usuari {user_obj.username}: {message}')
		elif action == 'reset_axes':
			reset_count = AxesProxyHandler.reset_attempts(username=user_obj.username)
			messages.success(request, f'S\'han reiniciat {reset_count} intents d\'Axes per a {user_obj.username}.')
		else:
			messages.error(request, 'Acció d\'usuari no vàlida.')

		query_string = f'?{urlencode({"q": users_q})}' if users_q else ''
		return redirect(f'{reverse(f"gestio:estadistiques_{section}")}{query_string}')

	if request.method == 'POST':
		if not can_manage_orders:
			messages.error(request, 'No tens permisos per canviar l\'estat de les comandes.')
			return redirect(f'gestio:estadistiques_{section}')

		comanda_id = request.POST.get('comanda_id')
		nou_estat = request.POST.get('nou_estat')
		valid_states = {choice for choice, _label in Comanda.Estat.choices}

		if nou_estat not in valid_states:
			messages.error(request, 'L\'estat seleccionat no és vàlid.')
			return redirect(f'gestio:estadistiques_{section}')

		comanda = get_object_or_404(Comanda, pk=comanda_id)
		comanda.estat = nou_estat
		comanda.save(update_fields=['estat', 'data_actualitzacio'])
		messages.success(request, f'Comanda #{comanda.pk} actualitzada a {comanda.get_estat_display()}.')
		return redirect(f'gestio:estadistiques_{section}')

	# Resum general de tots els vins en diccionari
	kpis = Vi.objects.aggregate(
		total_vins=Count('id'),
		stock_total=Sum('stock'),
		preu_mig=Avg('preu'),
		preu_min=Min('preu'),
		preu_max=Max('preu'),
	)
	# Estadístiques per tipus de vi, origen, stock i any de collita a través del ORM
	per_tipus_qs = (
		Vi.objects.values('tipus')
		.annotate(total=Count('id'))
		.order_by('tipus')
	)

	per_origen_qs = (
		Vi.objects.values('origen')
		.annotate(total=Count('id'))
		.order_by('origen')
	)

	top_stock_qs = (
		Vi.objects.values('nom', 'stock')
		.order_by('-stock')[:8]
	)

	per_any_qs = (
		Vi.objects.values('any_collita')
		.annotate(total=Count('id'))
		.order_by('any_collita')
	)
	# Transformem les consultes en format adequat per a les gràfiques (labels i values)
	per_tipus = {
		'labels': [item['tipus'] for item in per_tipus_qs],
		'values': [item['total'] for item in per_tipus_qs],
	}

	per_origen = {
		'labels': [item['origen'] for item in per_origen_qs],
		'values': [item['total'] for item in per_origen_qs],
	}

	top_stock = {
		'labels': [item['nom'] for item in top_stock_qs],
		'values': [item['stock'] for item in top_stock_qs],
	}

	per_any = {
		'labels': [item['any_collita'] for item in per_any_qs],
		'values': [item['total'] for item in per_any_qs],
	}
	
	context = { 
		'app_title': 'Estadístiques de vins',
		'section': section,
		'kpis' : kpis,
		'per_tipus' : per_tipus,
		'per_origen' : per_origen,
		'top_stock' : top_stock,
		'per_any' : per_any,
	}

	# Vendes: resum i llistats
	comandes_qs = Comanda.objects.select_related('user', 'direccio').prefetch_related('linies__vi').order_by('-data_creacio')
	comandes_by_status = {
		'estat_pendent': comandes_qs.filter(estat=Comanda.Estat.PENDENT),
		'estat_confirmada': comandes_qs.filter(estat=Comanda.Estat.CONFIRMADA),
		'estat_enviada': comandes_qs.filter(estat=Comanda.Estat.ENVIADA),
		'estat_entregada': comandes_qs.filter(estat=Comanda.Estat.ENTREGADA),
		'estat_cancelada': comandes_qs.filter(estat=Comanda.Estat.CANCELLADA),
	}
	completed_comandes_qs = comandes_qs.exclude(estat=Comanda.Estat.PENDENT)
	total_orders = completed_comandes_qs.count()
	total_revenue = completed_comandes_qs.aggregate(total=Sum('total'))['total'] or 0

	# Top vins venuts per unitats
	top_sold_qs = (
		LineaComanda.objects.values('vi__nom')
		.annotate(units_sold=Sum('unitats'))
		.order_by('-units_sold')[:8]
	)

	# Carret: items agrupats per usuari
	carret_items = Carret.objects.select_related('user', 'vi').all()
	carret_by_user = {}
	for item in carret_items:
		uname = item.user.username
		carret_by_user.setdefault(uname, {'user': item.user, 'items': []})
		carret_by_user[uname]['items'].append(item)
	carret_by_user = list(carret_by_user.values())

	# Usuaris: comptatge de comandes
	users_qs = User.objects.all().annotate(num_comandes=Count('comandes', distinct=True))
	if users_q:
		users_qs = users_qs.filter(
			Q(username__icontains=users_q)
			| Q(email__icontains=users_q)
			| Q(first_name__icontains=users_q)
			| Q(last_name__icontains=users_q)
		)
	users_qs = users_qs.order_by('username')
	users_list = []
	for user_obj in users_qs:
		users_list.append({
			'user': user_obj,
			'axes_locked': AxesProxyHandler.is_locked(request, credentials={'username': user_obj.username}),
		})

	# Afegim al context
	context.update({
		'comandes_recent': completed_comandes_qs[:12],
		'comandes_by_status': comandes_by_status,
		'estat_choices': Comanda.Estat.choices,
		'total_orders': total_orders,
		'total_revenue': total_revenue,
		'top_sold': {'labels': [i['vi__nom'] for i in top_sold_qs], 'values': [i['units_sold'] for i in top_sold_qs]},
		'carret_by_user': carret_by_user,
		'users_list': users_list,
		'users_q': users_q,
	})

	return render(request, 'gestio/estadistiques/estadistiques.html', context)