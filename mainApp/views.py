from django.shortcuts import redirect, render
from django.views import View
from .mixins import YouTube, YouTubeApi, YouTubeUploader
from django.contrib.auth import  logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm,CommentForm
from .models import Comment, ComentariosPagina,Profile, Infographics,CommentInfo,LogMultimedia
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from operator import itemgetter
from django.views.generic.edit import  UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.core.files.storage import default_storage
from django.conf import settings
import os
from moviepy.editor import VideoFileClip
from PIL import Image
from io import BytesIO
from django.core.exceptions import ValidationError
from django.core.files import File
import magic
from django.shortcuts import render, redirect
from .forms import LogMultimediaForm
from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

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
                return redirect('/accounts/login/')
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

class Blogs(View):
    def get(self, request):
        return render(request, 'blogs/blogs.html')
     
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




class DetallesInfografias(View):
    def get(self, request, id):
        infografia = get_object_or_404(Infographics, id=id)
        infografias_relacionadas = Infographics.objects.filter(category=infografia.category).exclude(id=id)
  
        comments = CommentInfo.objects.filter(info_id=infografia).order_by('timestamp')
        comment_form = CommentForm()

        main_comments = CommentInfo.objects.filter(info_id=infografia, parent_comment=None).order_by('timestamp')
        paginator = Paginator(main_comments, 3)
        page = request.GET.get('page')


        # Obtener los videos relacionados
        infografia = get_object_or_404(Infographics, id=id)
        video_ids_relacionados = infografia.supplementary_videos.values_list('video_id', flat=True)

        # Obtener datos de YouTube para un video específico
        videos_data = []
        for video_id in video_ids_relacionados:
            video_data = YouTubeApi().get_data(video_id)
            if video_data:
                videos_data.append(video_data)
        
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        context = {
            "infografia": infografia,
            "comments": comments,
            "comment_form": comment_form,
            "infografias_relacionadas": infografias_relacionadas,
            "videos": videos_data
        }

        return render(request, 'cursos/detallesInfografias.html', context)

    def post(self, request, id):
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid() and request.user.is_authenticated:
            text = comment_form.cleaned_data['text']
        
            new_comment = CommentInfo(user=request.user, info_id_id=id, text=text)
            new_comment.save()

            return redirect(reverse('detallesInfografia', kwargs={'id': id}))

        return redirect('detalles-infografia', id=id)


class ReplyCommentInfo(View):
    def post(self, request, id, comment_id):
        comment = get_object_or_404(CommentInfo, id=comment_id)

        reply_form = CommentForm(request.POST)

        if reply_form.is_valid() and request.user.is_authenticated:
            text = reply_form.cleaned_data['text']

            new_reply = CommentInfo(user=request.user, info_id_id=id, text=text, parent_comment=comment)
            new_reply.save()
       
        return redirect(reverse('detallesInfografia', kwargs={'id': id}))



@login_required
def signout(request):
    logout(request)
    messages.success(request, 'La sesión fue cerrada correctamente')
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




def is_valid_video(file):
    try:
            # Ejemplo: Validar que el archivo tiene una extensión de video permitida
            allowed_extensions = ['.mp4', '.avi', '.mkv']
            _, file_extension = os.path.splitext(file.name)
            if file_extension.lower() not in allowed_extensions:
                return False

            # Ejemplo adicional: Validar el contenido del archivo (puedes ajustar según tus necesidades)
            video_content = file.read()
            # Implementa tu lógica de validación aquí

            # Retorna True si el archivo es válido
            return True
    except Exception as e:
        print(f"Error al validar el video: {e}")
        return False

def is_valid_image(file):
    try:
        file_contents = file.read()
        img = Image.open(BytesIO(file_contents))
        return True
    except Exception as e:
        return False



    
def subirVideoImagen(request):
    if request.method == 'POST':
        form = LogMultimediaForm(request.POST, request.FILES)
        if form.is_valid():
            multimedia_instance = form.save(commit=False)
          
            # Verifica si el formato es 'video'
            if multimedia_instance.format == 1:  # 1 representa 'Video' en FormatCategory
                # Validar que el archivo sea un video
                if not is_valid_video(form.cleaned_data['file']):
                    messages.error(request, 'El archivo no es un video válido.')
                    return render(request, 'perfil/subirVideoImagen/subirVideoImagen.html', {'form': form})
              # Configuración de la conexión con la API de YouTube
                # youtube = build(
                #     settings.API_SERVICE_NAME,
                #     settings.API_VERSION,
                #     developerKey=settings.GOOGLE_API_KEY
                # )

                # # Información del video a subir
                # video_info = {
                #     'snippet': {
                #         'title': form.cleaned_data['title'],
                #         'description':form.cleaned_data['description'],
                #         'tags': [],  # Suponiendo que las etiquetas están separadas por comas en el formulario
                #         'categoryId': '27',  # Categoría de YouTube (puedes cambiarla según tus necesidades)
                #     },
                #     'status': {
                #         'privacyStatus': 'public',  # Puedes cambiar esto según tus necesidades (public, private, unlisted)
                #     },
                # }

                #  # Contenido del archivo
                # file_content = form.cleaned_data['file'].read()

                # # Subir el video
                # media_body = MediaIoBaseUpload(BytesIO(file_content), mimetype='video/*', chunksize=-1, resumable=True)
                # request = youtube.videos().insert(
                #     part=','.join(video_info.keys()),
                #     body=video_info,
                #     media_body=media_body
                # )

                # response = None
                # while response is None:
                #     status, response = request.next_chunk()
                #     if status:
                #         print(f'Subida del {int(status.progress() * 100)}% completada.')

                # print(f'Video subido exitosamente: {response["id"]}')


            # Verifica si el formato es 'imagen'
        
            elif multimedia_instance.format == 0:  # 0 representa 'Imagen' en FormatCategory
                # Validar que el archivo sea una imagen
                file = form.cleaned_data['file']
                if not is_valid_image(file):
                    messages.error(request, 'El archivo no es una imagen válida.')
                    return render(request, 'perfil/subirVideoImagen/subirVideoImagen.html', {'form': form})
              
                # Guarda la información en Infographics
                infographics_instance = Infographics(
                    user=User.objects.get(id=request.user.id),
                    title= form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    format=form.cleaned_data['format'],
                    file=form.cleaned_data['file'],
                    category=form.cleaned_data['category'],
                   
                )
                infographics_instance.save()

                supplementary_videos = form.cleaned_data['supplementary_videos']
                supplementary_Infographics = form.cleaned_data['supplementary_Infographics']
                
                infographics_instance.supplementary_videos.set(supplementary_videos)
                infographics_instance.supplementary_Infographics.set(supplementary_Infographics)
                infographics_instance.save() 

            messages.success(request, 'Se creo el contenido correctamente')
            return redirect('subirVideoImagen')  
    else:
       form = LogMultimediaForm(request.POST, request.FILES)
    
    return render(request, 'perfil/subirVideoImagen/subirVideoImagen.html', {'form': form})




    
    


def subirBlog(request):
    return render(request, 'perfil/subirBlog/subirBlog.html')

def administrarContenido(request):
    return render(request, 'perfil/administrarContenido/administrarContenido.html')

def notificaciones(request):
    return render(request, 'perfil/notificaciones/notificaciones.html')

def infografias(request):
    infografias_list = Infographics.objects.order_by('-timestamp')
    paginator = Paginator(infografias_list, 10)  
    page = request.GET.get('page')
    try:
        infografias = paginator.page(page)
    except PageNotAnInteger:
     
        infografias = paginator.page(1)
    except EmptyPage:
        infografias = paginator.page(paginator.num_pages)
    context = {'infografias': infografias}
    return render(request, 'cursos/infografias.html', context)

