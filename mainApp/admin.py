# mainApp/admin.py
from django.contrib import admin
from .models import Comment, ComentariosPagina, Profile

admin.site.register(Comment)
admin.site.register(ComentariosPagina)
admin.site.register(Profile)