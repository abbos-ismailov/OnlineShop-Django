from .models import Category, Product, MonthlyBestSeller
from apps.order.models import Wishlist, Cart


def main_data(request):
    categories = Category.objects.filter(is_active=True, parent=None)
    if request.user.is_authenticated:
        count_wish_list = Wishlist.objects.filter(user=request.user)
        cart = Cart.objects.filter(user=request.user, status='active').first()
        total_all_price = 0
        new_products = Product.objects.filter(is_active=True).order_by("-created_at")[
            :12
        ]
        monthlyBestSeller = MonthlyBestSeller.objects.filter(is_active=True).order_by(
            "-created_at"
        )[:2]

        if cart:
            cartItem = cart.cart_item_cart.all()

            for i in cartItem:
                total_all_price += i.total_price
        else:
            cartItem = []

        

        context = {
            "categories": categories,
            "new_products": new_products,
            "count_wish_list": count_wish_list,
            "cartItem": cartItem,
            "monthlyBestSeller": monthlyBestSeller,
            "total_all_price": total_all_price,
        }

        return context
    else:
        context = {
            "categories": categories,
            "count_wish_list": [],
            "cartItem": [],
            "total_all_price": 0,
        }

        return context