from django.db import models
from django.contrib.auth.models import User

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
    
category=[0,'Admin'],[1,'Usuario']
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)
    type_user=models.IntegerField(choices=category, default="1")
    def __str__(self):
        mapping_tipo_usuario = dict(category)
        tipo_usuario_str = mapping_tipo_usuario.get(self.type_user, 'Desconocido')
        return f'{self.user.username} - {tipo_usuario_str}'