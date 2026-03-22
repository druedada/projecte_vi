from django.shortcuts import render


def home(request):
	context = {
		'app_title': 'Inici'
	}
	return render(request, 'base.html', context)
