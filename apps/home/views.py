from django.shortcuts import render
from django.views.generic import View
from .models import Banner, BannerMiddle, BannerDiscount, Brands, MonthlyBestSeller, BannerBottom, Product
from datetime import datetime
# Create your views here.


class HomePageView(View):
    def get(self, request):
        banner = Banner.objects.filter(is_active=True).order_by("-created_at")[:3]
        middle_banner = BannerMiddle.objects.filter(is_active=True).last()
        discount_banner = BannerDiscount.objects.filter(deadline__gte=datetime.now(), is_active=True).order_by("-created_at")[:2]
        ### Yuqorida GTE dan foydalandik Lte ham bor Gte yuqorisini tekshiradi LTE vs GTE
        ### GTE vaqtdan tashqari boshqa narsalarni ham tekshiradimi
        brands = Brands.objects.filter(is_active=True).order_by("-created_at")
        monthlyBestSeller = MonthlyBestSeller.objects.filter(is_active=True).order_by("-created_at")[:2]
        bannerBottom = BannerBottom.objects.filter(is_active=True).last()
        product = Product.objects.filter(is_active=True).order_by('?')[:12]

        context = {
            "banner": banner,
            "banner_middle": middle_banner,
            "discount_banner": discount_banner,
            "brands": brands,
            "monthlyBestSeller": monthlyBestSeller,
            "bannerBottom": bannerBottom,
            'product': product
        }

        return render(request, "index.html", context)
