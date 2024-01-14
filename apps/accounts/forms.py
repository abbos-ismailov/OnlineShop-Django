from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', "placeholder": "+998908533642"}))
    password = forms.CharField(widget=PasswordInput(attrs={"placeholder":"Password"}))


class UserCreationForm(forms.ModelForm):
    first_name = forms.CharField(widget=TextInput(attrs={"placeholder": "First Name"}), required=True)
    last_name = forms.CharField(widget=TextInput(attrs={"placeholder": "Last Name"}), required=True)
    username = forms.CharField(widget=TextInput(attrs={"placeholder": "+998 90 853 3642"}), required=True)
    password = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Password"}), required=True)
    confirm_password = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Confirm Password"}), required=True)

    class Meta:
        model = User
        fields = ('first_name', "last_name", "username")

    def clean_username(self): ### Bu username xar hil zararli kodlarni kiritib yubormaslik uchun kerak
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu telefon raqam bilan oldin ro'yxatdan o'tilgan.")
        
        return username
    
    def clean_confirm_password(self):
        data = self.cleaned_data
        if data["password"] != data["confirm_password"]:
            raise forms.ValidationError("Parolingiz bir biriga teng bolishi kerak...")
        return data["confirm_password"]
    
    def save(self, commit=True):
        user = super().save(commit) ### commit Bu cash da saqlab turadi password hash langandan kiyin save qiladi
        user.set_password(self.cleaned_data["confirm_password"]) ### Mana shu joyida passwordni hash ladikmi
        user.save()
        
        return user


# class UpdateProfileForm(forms.ModelForm):
#     username = forms.CharField(widget=TextInput(attrs={'class': 'validate', "placeholder": "+998908533642"}))
#     first_name = forms.CharField(widget=PasswordInput(attrs={"placeholder":"First_name"}))