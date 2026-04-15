from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.vins.models import Vi
from .forms import ViForm
from django.db.models import Count, Sum, Avg, Min, Max


@login_required # Només usuaris autenticats poden accedir
@permission_required('vins.view_vi') # Només usuaris amb el permís de visualitzar vins poden accedir
def vins(request):   
	vins = Vi.objects.all().order_by('nom') # Obtenim tots els vins de la base de dades i els ordenem alfabèticament pel nom
	context = { # Context que es passarà al template per a renderitzar la pàgina del dashboard
		'app_title': 'Gestió de vins',
		'vins': vins,
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
def estadistiques(request):
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
		'kpis' : kpis,
		'per_tipus' : per_tipus,
		'per_origen' : per_origen,
		'top_stock' : top_stock,
		'per_any' : per_any,
	}

	return render(request, 'gestio/estadistiques/estadistiques.html', context)