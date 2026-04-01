
from django.shortcuts import render, redirect
from apps.vins.models import Vi

# Create your views here.



def carret(request):
	cart = request.session.get('cart', {})
	cart_items = []
	total = 0
	for vi_id, quantitat in cart.items():
		try:
			vi = Vi.objects.get(id=vi_id)
			subtotal = vi.preu * quantitat
			cart_items.append({
				'vi': vi,
				'quantitat': quantitat,
				'subtotal': subtotal
			})
			total += subtotal
		except Vi.DoesNotExist:
			continue
	context = {
		'app_title': 'Carret',
		'cart_items': cart_items,
		'total': total
	}
	return render(request, 'comandes/carret.html', context)
