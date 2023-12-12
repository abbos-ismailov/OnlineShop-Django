from django.contrib import admin
from .models import (
    Wishlist,
    Cart,
    CartItem,
    Order,
)
# Register your models here.

admin.site.register(Wishlist)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('user', 'status')
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('cart', 'status', 'created_at')