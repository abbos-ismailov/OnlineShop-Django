from .models import Category
from apps.order.models import Wishlist, Cart


def main_data(request):
    categories = Category.objects.filter(is_active=True, parent=None)
    count_wish_list = Wishlist.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user, status='active').first()
    total_all_price = 0
    if cart:
        cartItem = cart.cart_item_cart.all()

        for i in cartItem:
            total_all_price += i.total_price
    else:
        cartItem = []

    context = {
        "categories": categories,
        "count_wish_list": count_wish_list,
        "cartItem": cartItem,
        "total_all_price": total_all_price,
    }

    return context