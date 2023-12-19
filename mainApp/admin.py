# mainApp/admin.py
from django.contrib import admin
from .models import Comment, ComentariosPagina, Profile, Infographics,LogMultimedia

admin.site.register(Comment)
admin.site.register(ComentariosPagina)
admin.site.register(Profile)
admin.site.register(Infographics) 
admin.site.register(LogMultimedia)  