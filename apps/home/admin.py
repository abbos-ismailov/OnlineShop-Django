from django.contrib import admin
from .models import (
    Category,
    Brands,
    BannerBottom,
    Color,
    Tags,
    Size,
    Product,
    Banner,
    MonthlyBestSeller,
    BannerDiscount,
    BannerMiddle,
    ProductImage,
    AdditionalInfo,
    ProductReview,
)

from mptt.admin import DraggableMPTTAdmin
# Register your models here.

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'icon', 'img')
    list_display_links = ('indented_title', )


@admin.register(Size)
class SizeAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'name')
    list_display_links = ('indented_title', )
    
    
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass

@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    pass    


@admin.register(BannerBottom)
class BannerBottomAdmin(admin.ModelAdmin):
    pass

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass

@admin.register(MonthlyBestSeller)
class MonthlyBestSellerAdmin(admin.ModelAdmin):
    pass

@admin.register(BannerDiscount)
class BannerDiscountAdmin(admin.ModelAdmin):
    pass

@admin.register(BannerMiddle)
class BannerMiddleAdmin(admin.ModelAdmin):
    pass


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1
    

class AdditionalInfoAdmin(admin.TabularInline):
    model = AdditionalInfo
    extra = 1
    list_display = ['id', "key", 'product', "value"]
    list_filter = ['prodcut', 'created_at']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, AdditionalInfoAdmin]
    search_fields = ('title',)
    list_display = (
        'title', 'uuid'
    )

