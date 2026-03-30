from django import forms
from .models import Profile, OrderComment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# -------------------------
# REGISTRACIJOS FORMA
# -------------------------
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Įveskite komentarą..."
            })
        }

