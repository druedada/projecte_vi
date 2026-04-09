from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.vins.models import Vi
from .forms import ViForm


@login_required # Només usuaris autenticats poden accedir
@permission_required('vins.view_vi') # Només usuaris amb el permís de visualitzar vins poden accedir
def vins(request):   
	vins = Vi.objects.all().order_by('nom') # Obtenim tots els vins de la base de dades i els ordenem alfabèticament pel nom
	context = { # Context que es passarà al template per a renderitzar la pàgina del dashboard
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
