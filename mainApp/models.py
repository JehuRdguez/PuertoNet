from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=20)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'
    
class ComentariosPagina(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'
    
class Blogs(models.Model):
    titulo = models.TextField()
    imagenPortada = models.ImageField(upload_to='static/assets/img/blogs/')  # Ruta relativa a tu directorio de aplicaciones
    introduccion = models.TextField()
    contenido = models.TextField()
    autor = models.TextField(null=True, blank=True)  # Permitir nulo o configurar un valor predeterminado
    fecha = models.DateTimeField(default=datetime.now)
    
category=[0,'Admin'],[1,'Usuario']
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)
    type_user=models.IntegerField(choices=category, default="1")
    def __str__(self):
        mapping_tipo_usuario = dict(category)
        tipo_usuario_str = mapping_tipo_usuario.get(self.type_user, 'Desconocido')
        return f'{self.user.username} - {tipo_usuario_str}'
    
FormatCategory=[0,'Imagen'],[1,'Video'] 
CourseCategory=[0,'General'],[1,'Principiantes'],[3,'Kids'] 
class Infographics(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        title = models.CharField(max_length=255)
        description = models.TextField()
        format = models.IntegerField(choices=FormatCategory, default="0")
        file = models.FileField(upload_to='files/')
        category = models.IntegerField(choices=CourseCategory, default="0")
        supplementary_videos = models.ManyToManyField('LogMultimedia', blank=True)
        supplementary_Infographics = models.ManyToManyField('Infographics', blank=True)
        timestamp = models.DateTimeField(auto_now_add=True)
        def __str__(self):
            return f'{self.title} '
   
class CommentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info_id = models.ForeignKey( Infographics, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'  

class CommentBlog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_id = models.ForeignKey( Blogs, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'  

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    admin=models.ForeignKey(
     User,
        on_delete=models.CASCADE, related_name='Supervisor'
    )
       
    
   
class LogMultimedia(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    video_id = models.CharField(max_length=20)
    category = models.IntegerField(choices=CourseCategory, default="0")
    timestamp = models.DateTimeField(auto_now_add=True)
    supplementary_videos = models.ManyToManyField('LogMultimedia', blank=True)
    supplementary_Infographics = models.ManyToManyField('Infographics', blank=True)
    format = models.IntegerField(choices=FormatCategory, default="1")
    def __str__(self):
        return f'{self.title}'
