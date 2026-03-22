from django.shortcuts import render

# Create your views here.


def index(request):
	context = {
		'app_title': 'Subscripcions'
	}
	return render(request, 'base.html', context)
