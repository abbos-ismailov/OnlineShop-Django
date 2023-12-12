from django.db import models
from apps.base.models import BaseModel
from django.contrib.auth.models import User
# Create your models here.

STATUS_CART = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

STATUS_ORDER = (
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
)


class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_user')
    product = models.ForeignKey('home.Product', on_delete=models.CASCADE, related_name='wishlist_product')
    def __str__(self):
        return self.product.title

    
class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user')
    status = models.CharField(max_length=255, choices=STATUS_CART, default='active')
    def __str__(self):
        return self.user.username
    
    #### Nima uchun bu yerda total price hisoblanmadi

class CartItem(BaseModel):
    product = models.ForeignKey('home.Product', on_delete=models.CASCADE, related_name='cart_product')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item_cart')
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.product.title
    
    def save(self, *args, **kwargs):
        self.total_price = self.product.get_discount_price * self.quantity
        return super().save(*args, **kwargs)
  
class Order(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order_cart')
    status = models.CharField(max_length=255, choices=STATUS_ORDER, default='pending')
    
    def __str__(self) -> str:
        return self.cart.user.username
    
    
    