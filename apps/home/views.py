from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
import uuid
from .models import (
    Banner,
    BannerMiddle,
    BannerDiscount,
    Brands,
    BannerBottom,
    Product,
    Category,
    Color,
    ProductReview,
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

        brands = Brands.objects.filter(is_active=True).order_by("-created_at")

        bannerBottom = BannerBottom.objects.filter(is_active=True).last()
        product = Product.objects.filter(is_active=True).order_by("?")[:12]

        # popular_products = Product.objects.filter(is_active=True).order_by(
        #     "stars_percent"
        # )[:3]

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
            # "popular_products": popular_products,
            "hot_products": hot_products,
        }

        return render(request, "index.html", context)


class ParentCategory(View):
    def get(self, request, cat_uuid):  ####### Quyida __ ishlatdik <-----
        parent_cat_product = Product.objects.filter(
            is_active=True, category__uuid=cat_uuid
        ).order_by("-created_at")

        choosed_category = Category.objects.get(is_active=True, uuid=cat_uuid)
        if choosed_category.parent:
            choosed_category = choosed_category.parent.parent

        brands = Brands.objects.filter(is_active=True, category__uuid=cat_uuid)

        page_size = request.GET.get("page_size", 3)
        paginator = Paginator(parent_cat_product, page_size)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)

        color = Color.objects.filter(is_active=True)

        context = {
            "parent_cat_product": page_obj,
            "choosed_category": choosed_category,
            "brands": brands,
            "page_size": page_size,
            "colors": color,
            "checked_color": [],
            "checked_size": [],
        }
        return render(request, "parent_cat_product.html", context)

    def post(self, request, cat_uuid):
        parent_cat_product = Product.objects.filter(
            is_active=True, category__uuid=cat_uuid
        ).order_by("-created_at")

        choosed_category = Category.objects.get(is_active=True, uuid=cat_uuid)
        if choosed_category.parent:
            choosed_category = choosed_category.parent.parent

        brands = Brands.objects.filter(is_active=True, category__uuid=cat_uuid)

        color = Color.objects.filter(is_active=True)

        max_price = request.POST.get("price", []).split("-")[1]
        min_price = request.POST.get("price", []).split("-")[0]

        filter_request = {
            "color": list(map(uuid.UUID, request.POST.getlist("checkboxcolor"))),
            "size": list(map(uuid.UUID, request.POST.getlist("checkboxsize"))),
        }

        product_list = parent_cat_product.filter(
            (Q(price__gte=min_price) & Q(price__lte=max_price))
            & (
                Q(color__uuid__in=filter_request.get("color"))
                | Q(size__uuid__in=filter_request.get("size"))
            )
        )
        set_product_list = set(product_list)
        product_list = list(set_product_list)
        context = {
            "parent_cat_product": product_list,
            "choosed_category": choosed_category,
            "brands": brands,
            "colors": color,
            "checked_color": list(
                map(uuid.UUID, request.POST.getlist("checkboxcolor"))
            ),
            "checked_size": list(map(uuid.UUID, request.POST.getlist("checkboxsize"))),
        }
        return render(request, "parent_cat_product.html", context)


class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        product = get_object_or_404(Product, is_active=True, uuid=uuid)

        try:
            stars = int(stars)
            if 0 < stars <= 5:
                ProductReview.objects.create(
                    user=request.user,
                    product=product,
                    review=request.POST.get("comment"),
                    stars=stars,
                )

                return redirect(url)
            else:
                messages.error(
                    request,
                    "Yulduzlar soni faqat juft sonlar va 1 < n < 5 shartini qanoatlantirishi kerak VIEW",
                )
                return redirect(url)

        except:
            messages.error(
                request,
                "Yulduzlar soni faqat juft sonlar va 1 < n < 5 shartini qanoatlantirishi kerak VIEW",
            )
            return redirect(url)
            # raise forms.ValidationError("Yulduzlar soni faqat juft sonlar va 1 < n < 5 shartini qanoatlantirishi kerak VIEW")


class HeadCategoryFilterView(View):
    def get(self, request):
        category_uuid = request.GET.get("head_category_select")
        product_name = request.GET.get("head_search_product")

        choosed_category = Category.objects.get(is_active=True, uuid=category_uuid)
        if choosed_category.parent:
            choosed_category = choosed_category.parent

        if "/page" in product_name:
            product_name = product_name.split("/page")[0]

        choosed_products = Product.objects.filter(
            Q(is_active=True)
            & Q(category__uuid=category_uuid)
            & Q(title__icontains=product_name)
        )

        page_size = request.GET.get("page_size", 3)
        paginator = Paginator(choosed_products, page_size)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)

        brands = Brands.objects.filter(is_active=True, category__uuid=category_uuid)
        color = Color.objects.filter(is_active=True)
        # size =

        context = {
            "choosed_products": page_obj,
            "page_size": page_size,
            "brands": brands,
            "colors": color,
            "product_name": product_name,
            "choosed_category": choosed_category,
        }
        return render(request, "head_category_product.html", context)


class ProductViaBrandView(View):
    def get(self, request, brand_uuid):
        choosed_brand = Brands.objects.get(is_active=True, uuid=brand_uuid)
        choosed_category = choosed_brand.category

        choosed_products = Product.objects.filter(
            Q(is_active=True) & Q(brand__uuid=brand_uuid)
        )

        page_size = request.GET.get("page_size", 3)
        paginator = Paginator(choosed_products, page_size)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)

        color = Color.objects.filter(is_active=True)

        context = {
            "choosed_products": page_obj,
            "page_size": page_size,
            "colors": color,
            "choosed_category": choosed_category,
        }
        return render(request, "products_via_brand.html", context)

    def post(self, request, brand_uuid):
        choosed_products = Product.objects.filter(
            is_active=True, brand__uuid=brand_uuid
        )

        max_price = request.POST.get("price", []).split("-")[1]
        min_price = request.POST.get("price", []).split("-")[0]
        
        filter_request = {
            "color": list(map(uuid.UUID, request.POST.getlist("checkboxcolor"))),
            "size": list(map(uuid.UUID, request.POST.getlist("checkboxsize"))),
        }
        product_list = choosed_products.filter(
            (Q(price__gte=min_price) & Q(price__lte=max_price))
            & (
                Q(color__uuid__in=filter_request.get("color"))
                | Q(size__uuid__in=filter_request.get("size"))
            )
        )
        set_product_list = set(product_list)
        product_list = list(set_product_list)

        page_size = request.GET.get("page_size", 3)
        paginator = Paginator(product_list, page_size)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)

        color = Color.objects.filter(is_active=True)

        context = {
            "choosed_products": page_obj,
            "page_size": page_size,
            "colors": color,
            "checked_color": map(uuid.UUID, request.POST.getlist("checkboxcolor")),
            "checked_size": map(uuid.UUID, request.POST.getlist("checkboxsize")),
        }

        return render(request, "products_via_brand.html", context)
