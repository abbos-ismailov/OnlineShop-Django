from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Wishlist, Cart, CartItem, Order
from django import forms
from django.contrib import messages
from apps.home.models import Product, Color, Size
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class CreatedWishListView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        product = Product.objects.get(uuid=uuid)
        user = request.user

        if Wishlist.objects.filter(user=user, product=product):
            messages.warning(request, "Bu maxsulot yoqtirganlarda bor")
            return redirect(url)
        else:
            Wishlist.objects.create(product=product, user=user)  ### Filter
            messages.success(request, "Bu maxsulot yoqtirganlarga qo'shildi")

            return redirect(url)  ### Qaysi urlda turgan bolsa shu joyga qaytaradi


#### Zakaz qilish jarayoni
class CreateCartView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        product = Product.objects.get(uuid=uuid)
        user = request.user

        if Cart.objects.filter(user=user, status="active"):
            cart = Cart.objects.get(user=user, status="active")
            if CartItem.objects.filter(cart=cart, product=product):
                messages.warning(request, "Bu maxsulot bor")
                return redirect(url)
                ### Agar Cart va shu cart producti bolsa. Zakaz qilish jarayoni

            else:
                CartItem.objects.create(product=product, cart=cart)
                messages.success(request, "Savatchaga tushdi")
                return redirect(url)

        else:
            cart = Cart.objects.create(user=user)
            CartItem.objects.create(product=product, cart=cart)
            messages.success(request, "Savatchaga tushdi")
            return redirect(url)


class ProductDetailView(View):
    def get(self, request, uuid):
        choosed_item = get_object_or_404(Product, is_active=True, uuid=uuid)
        context = {
            "choosed_item": choosed_item,
        }
        return render(request, "product_detail.html", context)


class DeleteCartView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        url = request.META.get("HTTP_REFERER")

        if CartItem.objects.filter(uuid=uuid):
            cartItem = CartItem.objects.get(uuid=uuid)
            cartItem.delete()
            messages.success(request, "Mahsulotingiz o'chirildi")
            return redirect(url)

        else:
            messages.error(request ,"Bu mahsulot savatingizda yo'q")
            return redirect(url)


class CreateCartDetailView(LoginRequiredMixin, View):
    def post(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        product = Product.objects.get(uuid=uuid)
        user = request.user
        quantity = list(request.POST.get("product_quenty"))[0]

        try:
            quantity = int(quantity)
            if 0 > quantity or quantity > 10:
                raise forms.ValidationError(" Siz 0 < n < 10  ta olishingiz mumkin")

        except Exception as e:
            messages.error(request, f"Mahsulot soni butun bolishi kerak error: { e }")
            return redirect(url)

        if Cart.objects.filter(user=user, status="active"):
            cart = Cart.objects.get(user=user, status="active")
            if CartItem.objects.filter(cart=cart, product=product):
                messages.warning(request, "Bu maxsulot bor")
                return redirect(url)

            else:
                color = get_object_or_404(Color, uuid=request.POST.get("radiocolor"))
                size = get_object_or_404(Size, uuid=request.POST.get("radiosize"))

                CartItem.objects.create(
                    product=product,
                    cart=cart,
                    color=color,
                    size=size,
                    quantity=quantity,
                )
                messages.success(request, "Savatchaga tushdi")
                return redirect(url)

        else:
            color = get_object_or_404(Color, uuid=request.POST.get("radiocolor"))
            size = get_object_or_404(Size, uuid=request.POST.get("radiosize"))
            cart = Cart.objects.create(user=user)
            CartItem.objects.create(
                product=product, cart=cart, color=color, size=size, quantity=quantity
            )
            messages.success(request, "Savatchaga tushdi")
            return redirect(url)


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user.username
        cart = get_object_or_404(Cart, status="active", user__username = username)
        Order.objects.create(cart=cart)
        Cart.objects.filter(status="active", user__username = username).update(status="inactive")
        return redirect("accounts:profile")


class ShopWishlistView(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user.username
        shop_wishlist = Wishlist.objects.filter(is_active=True, user__username=username)
        context = {
            "shop_wishlist": shop_wishlist
        }
        return render(request, "shop-wishlist.html", context)


class DeleteWishView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        
        
        if Wishlist.objects.filter(product__uuid=uuid):
            wishItem = Wishlist.objects.filter(product__uuid=uuid)
            wishItem.delete()
            messages.success(request, "Mahsulotingiz o'chirildi")
            return redirect(url)

        else:
            messages.error(request ,"Bu mahsulot Wishlistingizda yo'q")
            return redirect(url)
    

class DetailCartView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            
        }
        return render(request, "shop-cart.html", context)

