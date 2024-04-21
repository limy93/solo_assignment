from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=63)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("country", "price")  # Adjust fields according to what you want to include in the form