from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView
from .forms import CustomAuthForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
# Create your views here.


class LoginView(View):
    form_class = CustomAuthForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("products:home")
        else:
            login_form = self.form_class

            return render(request, "accounts/login.html", {"login_form": login_form})

    def post(self, request):
        url = request.META.get("HTTP_REFERER")

        login_form = self.form_class(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()

            login(request, user)

            messages.success(request, "You have successfully log in.")
            return redirect("products:home")
        else:
            return render(request, "accounts/login.html", {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have succussfully Log out.")
        return redirect("products:home")


class RegisterView(View):
    form_class = UserCreationForm

    def get(self, request):
        create_form = self.form_class
        context = {"form": create_form}

        return render(request, "accounts/register.html", context)

    def post(self, request):
        create_form = self.form_class(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect("accounts:login")
        else:
            messages.error(request, f"{create_form.errors}")
            context = {"form": create_form}

            return render(request, "accounts/register.html", context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request): 
        user = User.objects.get(id=request.user.id)
        context = {
            "user": user
        }
        return render(request, "accounts/profile.html", context)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', "last_name", "username"]
    
    def get_success_url(self):
        return reverse_lazy("accounts:profile")

    template_name = "accounts/update_profile.html"
    
    def test_func(self): #### Nimaga buni ichiga kirmadi
        obj = self.get_object()
        print(obj, "Bu obj <-------------------------------")
        return obj.user == self.request.user