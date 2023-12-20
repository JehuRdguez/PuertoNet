# mainApp/admin.py
from django.contrib import admin
from .models import Comment, ComentariosPagina, Profile, Blogs, Infographics,LogMultimedia,Notifications

admin.site.register(Comment)
admin.site.register(ComentariosPagina)
admin.site.register(Blogs)
admin.site.register(Profile)
admin.site.register(Infographics) 
admin.site.register(LogMultimedia)  
admin.site.register(Notifications)
