from .views import _cart_id
from .models import Cart, CartItem

def item_count(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                print(request.user.is_authenticated)
                cart_items = CartItem.objects.filter(user=request.user)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                print(request.user.is_authenticated)
                cart_items = CartItem.objects.filter(cart=cart)
            for item in cart_items:
                count += item.quantity
        except Cart.DoesNotExist:
            count = 0
    return {
        "count": count
    }