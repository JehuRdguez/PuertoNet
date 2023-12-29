from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blogs, Profile, Infographics
from tinymce.widgets import TinyMCE
from .models import Profile, LogMultimedia

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
        
class LogImagenForm(forms.ModelForm):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    file = forms.FileField()
    

    class Meta:
        model = LogMultimedia
        fields = ['file', 'category', 'supplementary_videos', 'supplementary_Infographics','supplementary_Blogs']
        widgets = {
                'supplementary_videos': forms.CheckboxSelectMultiple(),
                'supplementary_Infographics': forms.CheckboxSelectMultiple(),
                'supplementary_Blogs': forms.CheckboxSelectMultiple(),
            }
        
        

class LogVideoForm(forms.ModelForm):
    class Meta:
        model = LogMultimedia
        fields = ['title','video_id', 'supplementary_videos', 'supplementary_Infographics','supplementary_Blogs']
        widgets = {
                'supplementary_videos': forms.CheckboxSelectMultiple(),
                'supplementary_Infographics': forms.CheckboxSelectMultiple(),
                 'supplementary_Blogs': forms.CheckboxSelectMultiple(),
            }
class EditInfographicsForm(forms.ModelForm):
    class Meta:
        model = Infographics
        fields = ['title', 'description', 'file', 'category', 'supplementary_videos', 'supplementary_Infographics', 'supplementary_Blogs']
        widgets = {
            'supplementary_videos': forms.CheckboxSelectMultiple(),
            'supplementary_Infographics': forms.CheckboxSelectMultiple(),
            'supplementary_Blogs': forms.CheckboxSelectMultiple(),
        }

class EditLogMultimediaForm(forms.ModelForm):
    class Meta:
        model = LogMultimedia
        fields = ['title',  'video_id', 'category', 'supplementary_videos', 'supplementary_Infographics', 'supplementary_Blogs']
        widgets = {
            'supplementary_videos': forms.CheckboxSelectMultiple(),
            'supplementary_Infographics': forms.CheckboxSelectMultiple(),
            'supplementary_Blogs': forms.CheckboxSelectMultiple(),
        }