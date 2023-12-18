from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator

from .models import (
    Banner,
    BannerMiddle,
    BannerDiscount,
    Brands,
    MonthlyBestSeller,
    BannerBottom,
    Product,
    Category,
)
from datetime import datetime


class HomePageView(View):
    def get(self, request):
        banner = Banner.objects.filter(is_active=True).order_by("-created_at")[:3]
        middle_banner = BannerMiddle.objects.filter(is_active=True).last()
        discount_banner = BannerDiscount.objects.filter(
            deadline__gte=datetime.now(), is_active=True
        ).order_by("-created_at")[:2]
        ### Yuqorida GTE dan foydalandik Lte ham bor Gte yuqorisini tekshiradi LTE vs GTE
        ### GTE vaqtdan tashqari boshqa narsalarni ham tekshiradimi
        brands = Brands.objects.filter(is_active=True).order_by("-created_at")
        
        bannerBottom = BannerBottom.objects.filter(is_active=True).last()
        product = Product.objects.filter(is_active=True).order_by("?")[:12]

        popular_products = Product.objects.filter(is_active=True).order_by(
            "stars_percent"
        )[:3]

        hot_products = Product.objects.filter(is_active=True, status="hot").order_by(
            "-created_at"
        )[:3]

        context = {
            "banner": banner,
            "banner_middle": middle_banner,
            "discount_banner": discount_banner,
            "brands": brands,
            "bannerBottom": bannerBottom,
            "product": product,
            "popular_products": popular_products,
            "hot_products": hot_products,
        }

        return render(request, "index.html", context)


class ParentCategory(View):
    def get(self, request, uuid):  ####### Quyida __ ishlatdik <-----
        parent_cat_product = Product.objects.filter(
            is_active=True, category__uuid=uuid
        ).order_by("-created_at")


        choosed_category = Category.objects.get(is_active=True, uuid=uuid)
        if choosed_category.parent:
            choosed_category = choosed_category.parent.parent
    
        brands = Brands.objects.filter(is_active=True, category__uuid=uuid)

        page_size = request.GET.get("page_size", 2)
        paginator = Paginator(parent_cat_product, page_size)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        context = {
            "parent_cat_product": page_obj,
            "choosed_category": choosed_category,
            "brands": brands,
        }
        return render(request, "parent_cat_product.html", context)