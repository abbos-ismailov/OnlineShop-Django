from django.urls import path, include
from .views import CreatedWishListView, CreateCartView, DeleteCartView

app_name = "order"

urlpatterns = [
    path('create-wishlist/<uuid:uuid>', CreatedWishListView.as_view(), name="create_wishlist"),
    path('create-cart/<uuid:uuid>', CreateCartView.as_view(), name="create_cart"),
    path('delete-cart-item/<uuid:uuid>', DeleteCartView.as_view(), name="delete_cart_item"),
]