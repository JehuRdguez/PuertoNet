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
    
<<<<<<< HEAD
class Blogs(models.Model):
    titulo = models.TextField()
    imagenPortada = models.ImageField(upload_to='static/assets/img/blogs/')  # Ruta relativa a tu directorio de aplicaciones
    introduccion = models.TextField()
    contenido = models.TextField()
    autor = models.TextField(null=True, blank=True)  # Permitir nulo o configurar un valor predeterminado
    fecha = models.DateTimeField(default=datetime.now)
=======
category=[0,'Admin'],[1,'Usuario']
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)
    type_user=models.IntegerField(choices=category, default="1")
    def __str__(self):
        mapping_tipo_usuario = dict(category)
        tipo_usuario_str = mapping_tipo_usuario.get(self.type_user, 'Desconocido')
        return f'{self.user.username} - {tipo_usuario_str}'
>>>>>>> e9872931c88987ba409439a8467c20b623eedacf
