from django.urls import path, include
from .views import HomePageView, ParentCategory

app_name = "products"

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('parent-cactegory/<uuid:uuid>', ParentCategory.as_view(), name="parent_category"),
]