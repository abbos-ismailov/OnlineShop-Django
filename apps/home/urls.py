from django.urls import path, include
from .views import HomePageView, ParentCategory, CreateCommentView, HeadCategoryFilterView, ProductViaBrandView

app_name = "products"

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('parent-cactegory/<uuid:cat_uuid>/', ParentCategory.as_view(), name="parent_category"),
    path('create-comment/<uuid:uuid>/', CreateCommentView.as_view(), name="create_comment"),
    path("head-category-filter/", HeadCategoryFilterView.as_view(), name="head_category_view"),
    path("products-via-brand/<uuid:brand_uuid>/", ProductViaBrandView.as_view(), name="products_via_brand")
]