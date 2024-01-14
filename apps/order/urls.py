from django.urls import path
from .views import (
    CreatedWishListView,
    CreateCartView,
    DeleteCartView,
    ProductDetailView,
    CreateCartDetailView,
    CreateOrderView,
    ShopWishlistView,
    DeleteWishView,
    DetailCartView,
)

app_name = "order"

urlpatterns = [
    path(
        "create-wishlist/<uuid:uuid>/",
        CreatedWishListView.as_view(),
        name="create_wishlist",
    ),
    path("shop-wishlist/", ShopWishlistView.as_view(), name="shop_wishlist"),
    path(
        "delete-wish-item/<uuid:uuid>/",
        DeleteWishView.as_view(),
        name="delete_wish_item",
    ),
    path("create-cart/<uuid:uuid>/", CreateCartView.as_view(), name="create_cart"),
    path(
        "delete-cart-item/<uuid:uuid>/",
        DeleteCartView.as_view(),
        name="delete_cart_item",
    ),
    path("detail-cart-view/", DetailCartView.as_view(), name="detail_cart"),
    path(
        "create-cart-detail/<uuid:uuid>/",
        CreateCartDetailView.as_view(),
        name="create_cart_detail",
    ),
    path(
        "product-detail/<uuid:uuid>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("create-order/", CreateOrderView.as_view(), name="create_order"),
]
