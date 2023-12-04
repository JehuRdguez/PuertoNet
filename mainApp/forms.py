from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=True)
    lastname = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'lastname', 'password1', 'password2']

class CommentForm(forms.Form):
    text = forms.CharField( widget=forms.Textarea(attrs={
            'class': 'form-control',
            'name': 'comentario',
            'placeholder': 'Cuéntanos tu opinión',
            'aria-label': 'With textarea',
            'rows': 2, 'cols': 30
        }))