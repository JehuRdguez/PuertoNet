# mainApp/admin.py
from django.contrib import admin
from .models import Comment, ComentariosPagina, Profile, Blogs, Infographics,LogMultimedia,Notifications,CommentBlog, APIKey

admin.site.register(Comment)
admin.site.register(ComentariosPagina)
admin.site.register(Blogs)
admin.site.register(Profile)
admin.site.register(Infographics) 
admin.site.register(LogMultimedia)  
admin.site.register(Notifications)
admin.site.register(CommentBlog)
admin.site.register(APIKey)
