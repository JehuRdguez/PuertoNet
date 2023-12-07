# mainApp/admin.py
from django.contrib import admin
from .models import Comment, ComentariosPagina

admin.site.register(Comment)
admin.site.register(ComentariosPagina)