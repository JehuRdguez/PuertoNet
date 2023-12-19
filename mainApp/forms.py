from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blogs
from tinymce.widgets import TinyMCE

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
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['titulo', 'imagenPortada', 'introduccion', 'contenido','autor']

    widgets = {
        'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        'imagenPortada': forms.FileInput(attrs={'class': 'form-control'}),
        'introduccion': forms.TextInput(attrs={'class': 'form-control'}),
        'contenido': TinyMCE(attrs={'class': 'form-control', 'rows': 10}),
        'autor': forms.TextInput(attrs={'class': 'form-control'}),
    }
