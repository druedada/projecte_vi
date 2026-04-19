from django.db.models import Sum

from apps.comandes.models import Carret


def cart_item_count(request):
    if request.user.is_authenticated:
        # Consulta directa al modelo para evitar posibles valores cacheados
        # del related manager sobre request.user.
        count = (
            Carret.objects.filter(user_id=request.user.id)
            .aggregate(total=Sum('unitats'))
            .get('total')
            or 0
        )
        return {'cart_item_count': count}

    # Fallback para posibles flujos anónimos basados en sesión.
    cart = request.session.get('cart', {})
    count = sum(item.get('quantity', 1) for item in cart.values()) if isinstance(cart, dict) else 0
    return {'cart_item_count': count}