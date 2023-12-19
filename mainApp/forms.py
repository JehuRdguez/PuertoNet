from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import PasswordChangeForm


class CommentForm(forms.Form):
    text = forms.CharField( widget=forms.Textarea(attrs={
            'class': 'form-control',
            'name': 'comentario',
            'placeholder': 'Cuéntanos tu opinión',
            'aria-label': 'With textarea',
            'rows': 2, 'cols': 30
        }))
    

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=True)
    lastname = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'lastname', 'password1', 'password2']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Selecciona una imagen'})
        
