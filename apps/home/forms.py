from django import forms
from django.forms.widgets import TextInput
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=TextInput(attrs={"placeholder": "Write Comment"}), required=True)
    stars = forms.CharField(widget=TextInput(attrs={"placeholder": "Stars"}))
   
    def clean_stars(self): ### Negadir ishlamadi
        stars = self.cleaned_data["stars"]
        print(stars, "============================ This is star")
        
        if isinstance(stars, int) and 0 < stars <= 5: 
            return stars
        else:
            raise forms.ValidationError("Yulduzlar soni faqat juft sonlar va 1 < n < 5 shartini qanoatlantirishi kerak.........")