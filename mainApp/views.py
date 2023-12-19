from django.shortcuts import redirect, render
from django.views import View
from .mixins import YouTube
from django.contrib.auth import  logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm,CommentForm
from .models import Comment, ComentariosPagina, Blogs
from .models import Comment, ComentariosPagina,Profile
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from operator import itemgetter
from .forms import BlogForm
from django.contrib.auth.models import User
from django.views.generic.edit import  UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.core.files.storage import default_storage
from django.conf import settings
import os


@login_required
def editarUsuario(request):
    user = request.user
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_lastname = request.POST.get('lastname')
        new_email = request.POST.get('email')
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')
        new_image = request.FILES.get('image')
        
        user.first_name = new_name
        user.last_name = new_lastname
        user.save()

        if new_email != user.email:
            try:
                User.objects.exclude(pk=user.pk).get(email=new_email)
                messages.error(request, 'El correo electrónico ya está en uso.')
            except User.DoesNotExist:
                user.email = new_email
                user.save()
                messages.success(request, 'Cambios guardados exitosamente.')

        if new_image:
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                usuario = request.user.id
                cuenta = Profile.objects.create(user_id=usuario, image=new_image)
                messages.success(request, 'Cambios guardados exitosamente.')
            else:
                if profile.image:
                    file_path = os.path.join(settings.MEDIA_ROOT, str(profile.image))
                    default_storage.delete(file_path)

                profile.image = new_image
                profile.save()
                messages.success(request, 'Cambios guardados exitosamente.')
            
        if new_password1:
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                messages.success(request, 'Los cambios se aplicaron, inicia sesión')
                return redirect('/')
            else: 
                messages.error(request, 'Las contraseñas no coinciden')
        else:
            messages.success(request, 'Se aplicaron los cambios correctamente')
        return redirect('editarUsuario')  
    return render(request, 'perfil/editarUsuario/editarUsuario.html')



class inicio(View):
   def get(self, request):
        comentarios = ComentariosPagina.objects.all()
        YaHaComentado = request.session.pop('YaHaComentado', False)
        return render(request, 'inicio.html', {'comentarios': comentarios,'YaHaComentado': YaHaComentado})
    
class historia(View):
    def get(self, request):
        return render(request, 'historia/historia.html')
    
class avisoprivacidad(View):
    def get(self, request):
        return render(request, 'avisoprivacidad/avisoprivacidad.html')
    
class terminoscondiciones(View):
    def get(self, request):
        return render(request, 'terminos/terminos_condiciones.html')   

class soporte(View):
    def get(self, request):
        return render(request, 'soporte/soporte.html')  

class BlogsPagina(View):
    def get(self, request):
        blogs = Blogs.objects.all()
        return render(request, 'blogs/blogs.html',{'datos':blogs})
    
class TemplateBlog(View):
    def get(self, request, blog_id):
        blogs = Blogs.objects.get(id=blog_id)
        return render(request, 'blogs/template_blogs.html',{'datos':blogs})

     
class cursos(View):
    def get(self, request):
        categoria = request.GET.get('categoria', None)

        videos = YouTube().get_data()

        # Ordena los videos por el título
        videos = sorted(videos, key=itemgetter('fecha'), reverse=True)

        # Obtén todas las categorías de todos los videos y conviértelas en una lista plana
        all_categories = list(chain.from_iterable(v.get('categoria', []) for v in videos))

        # Elimina duplicados manteniendo el orden original
        unique_categories = sorted(set(all_categories), key=all_categories.index)

        # Implementa la paginación
        paginator = Paginator(videos, 10)  # Muestra 10 videos por página
        page = request.GET.get('page', 1)

        try:
            videos_pagina = paginator.page(page)
        except PageNotAnInteger:
            videos_pagina = paginator.page(1)
        except EmptyPage:
            videos_pagina = paginator.page(paginator.num_pages)
        context = {"videos": videos_pagina, "unique_categories": unique_categories, "categoria_seleccionada": categoria, "rango": range(1, paginator.num_pages + 1)}
        return render(request, 'cursos/cursos.html', context)
    
class cursosOrden(View):
    def get(self, request):
        categoria = request.GET.get('categoria', None)

        videos = YouTube().get_data()

        # Ordena los videos por el título
        videos = sorted(videos, key=itemgetter('title'))

        # Obtén todas las categorías de todos los videos y conviértelas en una lista plana
        all_categories = list(chain.from_iterable(v.get('categoria', []) for v in videos))

        # Elimina duplicados manteniendo el orden original
        unique_categories = sorted(set(all_categories), key=all_categories.index)

        # Implementa la paginación
        paginator = Paginator(videos, 9)  # Muestra 10 videos por página
        page = request.GET.get('page', 1)

        try:
            videos_pagina = paginator.page(page)
        except PageNotAnInteger:
            videos_pagina = paginator.page(1)
        except EmptyPage:
            videos_pagina = paginator.page(paginator.num_pages)
        
        context = {"videos": videos_pagina, "unique_categories": unique_categories, "categoria_seleccionada": categoria, "rango": range(1, paginator.num_pages + 1)}
        return render(request, 'cursos/cursos.html', context)

def videos(request):

	videos = YouTube().get_data()

	context = {"videos": videos}
	return render(request, 'videos.html', context)

 
'''
Basic view for showing a video in an iframe 
'''
# def play_video(request):
#     videos = YouTube().get_data()
#     vid_id = request.GET.get("vid_id")

#     vid_data = YouTube(vid_id=vid_id).get_video()

#     contextUno = {
#         "vid_data": vid_data,
#     	"videos": videos
#     }



#     return render(request, 'play_video.html', contextUno)


class play_video(View):
    def get(self, request, vid_id):

        videos = YouTube().get_data()  
        vid_data = YouTube(vid_id=vid_id).get_video()
       
        comments = Comment.objects.filter(video_id=vid_id).order_by('timestamp')
        comment_form = CommentForm()
        
        
        #  Problema en paginación
        main_comments = Comment.objects.filter(video_id=vid_id, parent_comment=None).order_by('timestamp')
        paginator = Paginator(main_comments, 3)
        page = request.GET.get('page')

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        contextUno = {
            "vid_data": vid_data,
            "videos": videos,
            "comments": comments,
            "comment_form": comment_form,
        }
        

        return render(request, 'cursos/play_video.html', contextUno)

    def post(self, request, vid_id):
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid() and request.user.is_authenticated:
            text = comment_form.cleaned_data['text']
            new_comment = Comment(user=request.user, video_id=vid_id, text=text)
            new_comment.save()

            return redirect(reverse('play-video', kwargs={'vid_id': vid_id}))

        return redirect('play-video', vid_id=vid_id)






class ReplyComment(View):
    def post(self, request, vid_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        reply_form = CommentForm(request.POST)

        if reply_form.is_valid() and request.user.is_authenticated:
            text = reply_form.cleaned_data['text']

            new_reply = Comment(user=request.user, video_id=vid_id, text=text, parent_comment=comment)
            new_reply.save()
       
        return redirect(reverse('play-video', kwargs={'vid_id': vid_id}))





@login_required
def signout(request):
    logout(request)
    return redirect('/')



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            lastname = form.cleaned_data['lastname']
            
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(request, 'Ya existe un usuario con este nombre de usuario o correo electrónico.')
            else:
                user = form.save(commit=False)
                user.first_name = name
                user.last_name = lastname
                user.save()

                authenticated_user = authenticate(request, username=username, password=form.cleaned_data['password1'])
                login(request, authenticated_user)
                usuario = request.user.id
                profile = Profile.objects.create(user_id=usuario)
                return redirect('/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'account/signup.html', {'form': form})

def conocenos(request):
    return render(request, 'conocenos/conocenos.html')




def comentarioPagina(request):
    if ComentariosPagina.objects.filter(user=request.user).exists():
        request.session['YaHaComentado'] = True
        return redirect('/')

    if request.method == 'POST':
        comentarioTexto = request.POST.get('comentarioTexto', '')
        if comentarioTexto and len(comentarioTexto) <= 220:
            comentario = ComentariosPagina.objects.create(user=request.user, text=comentarioTexto)
            messages.success(request, '¡Gracias por comentar!')
            return redirect('/')
        elif not comentarioTexto:
            messages.error(request, 'El comentario no puede estar vacío.')
        else:
            messages.error(request, 'El comentario no puede tener más de 220 caracteres.')

    return redirect('/')





    
    
def subirVideoImagen(request):
    return render(request, 'perfil/subirVideoImagen/subirVideoImagen.html')

def subirBlog(request):
    blogs = Blogs.objects.all()
    usuario_autenticado = request.user
    # Filtra la consulta para obtener solo el usuario autenticado
    usuario = User.objects.get(username=usuario_autenticado.username)
    # Asocia el usuario autenticado al blog antes de guardar
    usuario = f"{usuario.first_name} {usuario.last_name}"
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            blog = form.save()

            messages.success(request, "Blog subido exitosamente.")
            return redirect('subirBlog')  # Ajusta según tu aplicación
        else:
            print(form.errors)
            messages.error(request, "Error al subir blog. Verifica los datos.")
    else:
        form = BlogForm()

    return render(request, 'perfil/subirBlog/subirBlog.html', {'form': form, 'datos': blogs,'user':usuario})


#def subirBlog(request):    
#    if request.method == 'POST':
#        try:
#            titulo = request.POST.get('titulo')
#            print(titulo)
#            return render(request, 'perfil/subirBlog/subirBlog.html')
#        except Exception as e:
#            messages.error(request, "Error al subir blog")
#            return render(request, 'perfil/subirBlog/subirBlog.html')
#    return render(request, 'perfil/subirBlog/subirBlog.html')
#

def administrarContenido(request):
    return render(request, 'perfil/administrarContenido/administrarContenido.html')

def notificaciones(request):
    return render(request, 'perfil/notificaciones/notificaciones.html')
