from django.db import models
from apps.base.models import BaseModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.db.models import Avg
from django.contrib.auth.models import User


STATUS = (
    ('new', 'NEW'),
    ('hot', 'HOT'),
    ('best', 'BEST SELL'),
    ('sale', 'SALE'),
)

class Size(MPTTModel, BaseModel):
    name = models.CharField(max_length=120)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

   
    def __str__(self):
        return self.name

class Category(MPTTModel, BaseModel):
    name = RichTextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.ImageField(upload_to='category/icons', null=True, blank=True)
    img = models.ImageField(upload_to='category/images', null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, related_name="size_category")

    def __str__(self):
        return self.name
        
        
    
class Brands(BaseModel):
    name = models.CharField(max_length=120)
    img = models.FileField(upload_to='brands/images', null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name="category_to_brand")

    def __str__(self):
        return self.name
    
    

    
class BannerBottom(BaseModel):
    name = RichTextField()
    img = models.ImageField(upload_to='banner/images', null=True, blank=True)
    def __str__(self):
        return self.name
    
    
class Color(BaseModel):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=120, null=True, blank=True)
    def __str__(self):
        return self.name

    
class Tags(BaseModel):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name






class Product(BaseModel):
    category = models.ManyToManyField(Category, related_name="category_products")
    title = models.CharField(max_length=255)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, null=True, blank=True, related_name='products_brand')
    price = models.BigIntegerField()
    discount = models.IntegerField(default=0)
    description = RichTextField()
    color = models.ManyToManyField(Color, blank=True, related_name='products_color')
    size = models.ManyToManyField(Size, blank=True, related_name='products_size')
    quenty = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tags, blank=True, related_name='products_tags')
    discription_main = RichTextField()
    status = models.CharField(max_length=255, choices=STATUS, default='new')
    # stars_percent = models.IntegerField()
    
    @property
    def get_discount_price(self):
        if self.discount:
            result = self.price - (self.price * self.discount)/100
            return result
        else:
            return self.price

    @property
    def mid_stars(self):
        result = ProductReview.objects.filter(product=self.uuid).aggregate(avarage=Avg("stars"))
        if result['avarage']:
            return round(result['avarage'], 1)
        else:
            return 0

    @property
    def mid_stars_percent(self):
        result = ProductReview.objects.filter(product=self.uuid).aggregate(avarage=Avg("stars"))
        if result['avarage']:
            percent = result['avarage'] * 100 / 5
            self.stars_percent = int(percent)
            return int(percent)
        else:
            return 0

    
    def __str__(self) -> str:
        return self.title
    
    
class Banner(BaseModel):
    
    name = RichTextField()
    img = models.ImageField(upload_to='banner/images', null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.name
    
    
    
class MonthlyBestSeller(BaseModel):
    
    name = RichTextField()
    img = models.ImageField(upload_to='banner/images', null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    def __str__(self):
        return self.name  

    
    
class BannerDiscount(BaseModel):
    name = RichTextField()
    img = models.ImageField(upload_to='banner/images', null=True, blank=True)
    deadline = models.DateTimeField()
    products = models.ManyToManyField(Product, blank=True, related_name="products_banner_discount")
    def __str__(self):
        return self.name
    
    
    
class BannerMiddle(BaseModel):
    
    name = RichTextField()
    img = models.ImageField(upload_to='banner/images', null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    def __str__(self):
        return self.name
    
    
class ProductImage(BaseModel):
    img = models.ImageField(upload_to='product/images', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='product_image')
    
    def __str__(self) -> str:
        return self.product.title
    
class AdditionalInfo(BaseModel):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='product_additional_info')
    
    def __str__(self) -> str:
        return self.product.title
    
class ProductReview(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='product_review_user')
    review = models.TextField()
    stars = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='product_review')
    
    def stars_percent(self):
        percent = self.stars * 20
        return percent 
    
    def __str__(self) -> str:
        return self.product.title