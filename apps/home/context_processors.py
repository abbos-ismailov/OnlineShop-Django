from .models import Category, Product, MonthlyBestSeller
from apps.order.models import Wishlist, Cart, Order


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
        
        order = Order.objects.filter(status="pending", is_active=True, cart__user=request.user).order_by("-created_at").first()        

        context = {
            "categories": categories,
            "new_products": new_products,
            "count_wish_list": count_wish_list,
            "cartItem": cartItem,
            "cart": cart,
            "monthlyBestSeller": monthlyBestSeller,
            "total_all_price": total_all_price,
            "order_items": order ############ ORDER qilish kerak shu joyida error BErdi 
        }

        return context
    else:
        context = {
            "categories": categories,
            "count_wish_list": [],
            "cartItem": [],
            "cart": None,
            "total_all_price": 0,
            "order_items": []
        }

        return context