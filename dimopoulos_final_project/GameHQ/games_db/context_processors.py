from .models import ShoppingCart

def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = ShoppingCart.objects.get(user=request.user)
            return {'cart_count': sum(item.quantity for item in cart.cart_items.all())}
        except ShoppingCart.DoesNotExist:
            return {'cart_count': 0}
    return {'cart_count': 0}