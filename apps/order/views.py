from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Wishlist, Cart, CartItem
from django.contrib import messages
from apps.home.models import Product
# Create your views here.

class CreatedWishListView(View):
    def get(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        product = Product.objects.get(uuid=uuid)
        user = request.user

        if Wishlist.objects.filter(user=user, product=product):
            messages.warning(request, "Bu maxsulot yoqtirganlarda bor")
            return redirect(url) 
        else:
            Wishlist.objects.create(product=product, user=user) ### Filter
            messages.success(request, "Bu maxsulot yoqtirganlarga qo'shildi")

            return redirect(url) ### Qaysi urlda turgan bolsa shu joyga qaytaradi

#### Zakaz qilish jarayoni
class CreateCartView(View):
    def get(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        product = Product.objects.get(uuid=uuid)
        user = request.user

        

        if Cart.objects.filter(user=user, status='active'):
            cart = Cart.objects.get(user=user, status='active')
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
        
class DeleteCartView(View):
    def get(self, request, uuid):
        url = request.META.get('HTTP_REFERER')

        if CartItem.objects.filter(uuid=uuid):
            cartItem = CartItem.objects.get(uuid=uuid)
            cartItem.delete()
            messages.success(request, "Mahsulotingiz o'chirildi")
            return redirect(url)
        
        else:
            messages.error("Bu mahsulot savatingizda yo'q")
            return redirect(url)