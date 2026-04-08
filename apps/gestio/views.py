from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.vins.models import Vi

from .forms import ViForm


@login_required
@permission_required('vins.view_vi')
def dashboard(request):
	vins = Vi.objects.all().order_by('nom')
	context = {
		'app_title': 'Gestio de vins',
		'vins': vins,
	}
	return render(request, 'gestio/vins/dashboard.html', context)


@login_required
@permission_required('vins.view_vi')
def llistar_vins(request):
	vins = Vi.objects.all().order_by('nom')
	context = {
		'app_title': 'Llista de vins',
		'vins': vins,
	}
	return render(request, 'gestio/vins/llista.html', context)


@login_required
@permission_required('vins.add_vi')
def crear_vi(request):
	if request.method == 'POST':
		form = ViForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('gestio:dashboard')
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
	vi = get_object_or_404(Vi, pk=vi_id)
	if request.method == 'POST':
		form = ViForm(request.POST, request.FILES, instance=vi)
		if form.is_valid():
			form.save()
			return redirect('gestio:dashboard')
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
		vi.delete()
		return redirect('gestio:dashboard')
	return redirect('gestio:dashboard')
