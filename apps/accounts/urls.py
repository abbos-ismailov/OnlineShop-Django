from django.urls import path
from .views import LoginView, LogoutView, RegisterView, ProfileView, UpdateProfileView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path("update/<int:pk>", UpdateProfileView.as_view(), name="update"),

    path('password_change/', PasswordChangeView.as_view(), name="password_change"), ### Password changing started
    path('password_change/done/', PasswordChangeDoneView.as_view(), name="password_change_done"), ### Template 
]