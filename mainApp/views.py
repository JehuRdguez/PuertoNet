from django.shortcuts import redirect, render
from django.views import View
from .mixins import YouTube, YouTubeApi, YouTubeUploader
from django.contrib.auth import  logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm,CommentForm

from .models import Comment, ComentariosPagina,Profile, Infographics,CommentInfo,LogMultimedia, Blogs, Notifications, CommentBlog
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from operator import itemgetter
from .forms import BlogForm,EditInfographicsForm, EditLogMultimediaForm
from django.contrib.auth.models import User
from django.views.generic.edit import  UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.core.files.storage import default_storage
from django.conf import settings
import os
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.template.loader import get_template
import uuid
from django.core.files.storage import default_storage
from moviepy.editor import VideoFileClip
from PIL import Image
from io import BytesIO
from django.core.exceptions import ValidationError
from django.core.files import File
from django.shortcuts import render, redirect
from .forms import LogImagenForm, LogVideoForm
from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
 
def is_valid_image(file):
    try:
        file_contents = file.read()
        img = Image.open(BytesIO(file_contents))
        return True
    except Exception as e:
        return False
    
class InfographicsUpdateView(UpdateView):
    model = Infographics
    form_class=EditInfographicsForm
    template_name = 'infografias/editarInfografia.html'  
    success_url = reverse_lazy('administrarContenido')
    def form_valid(self, form):
        file = self.request.FILES.get('file')
        if file and not is_valid_image(file):
            return self.form_invalid(form)
      
        messages.success(self.request, '¡Actualización exitosa!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error en la actualización. Por favor, verifica los datos.')
        return super().form_invalid(form)

class LogMultimediaUpdateView(UpdateView):
    model = LogMultimedia
    form_class = EditLogMultimediaForm  
    template_name = 'cursos/editarVideo.html'  
    success_url = reverse_lazy('administrarContenido')
    def form_valid(self, form):
        messages.success(self.request, '¡Actualización exitosa!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error en la actualización. Por favor, verifica los datos.')
        return super().form_invalid(form)
    
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
    
    def post(self, request, *args, **kwargs):
        try:
            subject = 'Soporte PuertoNet'
            template_usuario = get_template('soporte/templateCorreo.html')
            template_host = get_template('soporte/templateSoporte.html')  # Nueva plantilla para el host
            correo = request.POST['correo']
            descripcion = request.POST['descripcion']
            imagen = request.FILES.get('imagen')

            # Inicializar la variable de la URL de la imagen
            imagen_url = None

            # Verificar si se proporcionó una imagen
            if imagen:
                # Define el nombre único del archivo (por ejemplo, utilizando UUID)
                nombre_archivo = f"{uuid.uuid4()}.{imagen.name.split('.')[-1]}"

                # Guarda la imagen en la carpeta designada
                ruta_archivo = default_storage.save(f'tu_carpeta/{nombre_archivo}', imagen)

                # Obtén la URL de la imagen guardada
                imagen_url = default_storage.url(ruta_archivo)

            # Renderizar el contenido para el usuario
            content_usuario = template_usuario.render(
                {'problema': descripcion, 'imagen_url': imagen_url}
            )

            # Renderizar el contenido para el host
            content_host = template_host.render(
                {'problema': descripcion, 'correo': correo, 'imagen_url': imagen_url}
            )

            # Crear el mensaje para el usuario
            message_usuario = EmailMultiAlternatives(
                subject,
                '',  # Dejé el campo en blanco porque estás adjuntando HTML
                settings.EMAIL_HOST_USER,
                [correo]
            )

            # Adjunta la imagen al correo si se proporcionó
            if imagen_url:
                message_usuario.attach_file(default_storage.path(ruta_archivo))

            message_usuario.attach_alternative(content_usuario, 'text/html')
            message_usuario.send()

            # Crear el mensaje para el host
            message_host = EmailMultiAlternatives(
                subject,
                '',  # Dejé el campo en blanco porque estás adjuntando HTML
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER]  # Solo al host
            )

            message_host.attach_alternative(content_host, 'text/html')
            message_host.send()

            # Borra la imagen del servidor si se proporcionó
            if imagen_url:
                default_storage.delete(ruta_archivo)

            messages.success(request, "Correo enviado con éxito.")
            return redirect('Soporte')  # Redirigir a una página de éxito después de enviar el correo
        except ValidationError as e:
            # Manejar errores de validación
            messages.error(request, "Error de validación al enviar el correo")
            return render(request, 'soporte/soporte.html', {'error': 'Error de validación al enviar el correo'})
        except Exception as e:
            # Manejar otros errores
            messages.error(request, "Error al enviar el correo")
            return render(request, 'soporte/soporte.html', {'error': 'Error al enviar el correo'})



class BlogsPagina(View):
    def get(self, request):
        blogs = Blogs.objects.all()

        paginator = Paginator(blogs, 3)  # Muestra 10 videos por página
        page = request.GET.get('page', 1)
        try:
            blogs  = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        return render(request, 'blogs/blogs.html',{'datos':blogs,"rango": range(1, paginator.num_pages + 1)})

class TemplateBlog(View):
    def get(self, request, blog_id):
        blogs = Blogs.objects.get(id=blog_id)
        comments = CommentBlog.objects.filter(blog_id=blog_id).order_by('timestamp')
        comment_form = CommentForm()
        main_comments = CommentBlog.objects.filter(blog_id=blog_id, parent_comment=None).order_by('timestamp')
        paginator = Paginator(main_comments, 3)
        page = request.GET.get('page')
        
        comentarioReplay = CommentBlog.objects.filter(blog_id=blog_id).exclude(parent_comment=None)
        print(comentarioReplay)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        contextUno = {
            'datos':blogs,
            "comments": comments,
            "comentarioReplay":comentarioReplay,
            "comment_form": comment_form,
        }
        return render(request, 'blogs/template_blogs.html',contextUno)
    
    def post(self, request, blog_id):
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid() and request.user.is_authenticated:
            text = comment_form.cleaned_data['text']
            # Obtén la instancia del blog usando get_object_or_404
            blog_instance = get_object_or_404(Blogs, pk=blog_id)
            new_comment = CommentBlog(user=request.user, blog_id=blog_instance, text=text)
            new_comment.save()

            return redirect(reverse('Blog', kwargs={'blog_id': blog_id}))

        return redirect('Blog', blog_id=blog_id)
     
class ReplyCommentBlog(View):
    def post(self, request, id, comment_id):
        comment = get_object_or_404(CommentBlog, id=comment_id)

        reply_form = CommentForm(request.POST)

        if reply_form.is_valid() and request.user.is_authenticated:
            text = reply_form.cleaned_data['text']
            
            # Obtén la instancia del blog usando get_object_or_404
            blog_instance = get_object_or_404(Blogs, pk=id)

            new_reply = CommentBlog(user=request.user, blog_id=blog_instance, text=text, parent_comment=comment)
            new_reply.save()
            
            Blog = Blogs.objects.filter(id=id).first()
            description = "Hay nuevos comentarios en " + Blog.titulo
            admin = request.user
            new_notification = Notifications(user=request.user, description=description, admin=admin)
            new_notification.save()
       
        return redirect(reverse('Blog', kwargs={'blog_id': id}))
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

class play_video(View):
    def get(self, request, vid_id):

        videos = YouTube().get_data()  
        vid_data = YouTube(vid_id=vid_id).get_video()
        InfoVideos=get_object_or_404(LogMultimedia,video_id=vid_id)
        comments = Comment.objects.filter(video_id=vid_id).order_by('timestamp')
        comment_form = CommentForm()
        videos_relacionados = LogMultimedia.objects.filter(category=InfoVideos.category).exclude(id=InfoVideos.id).values_list('video_id', flat=True)
        
        
        video_ids_relacionados =InfoVideos.supplementary_videos.values_list('video_id', flat=True)

        # Obtener datos de YouTube para un video específico
        videos_data = []
        for video_id in video_ids_relacionados:
            video_data = YouTubeApi().get_data(video_id)
            if video_data:
                videos_data.append(video_data)
                
        videos_data_relacionados = []
        for video_id in videos_relacionados:
            video_data_relacionados = YouTubeApi().get_data(video_id)
            if video_data_relacionados:
                videos_data_relacionados.append(video_data_relacionados)
      
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
            "InfoVideos":InfoVideos,
            "videos_data":videos_data,
            "videos_relacionados": videos_data_relacionados
        }
        

        return render(request, 'cursos/play_video.html', contextUno)

    def post(self, request, vid_id):
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid() and request.user.is_authenticated:
            text = comment_form.cleaned_data['text']
            new_comment = Comment(user=request.user, video_id=vid_id, text=text)
            new_comment.save()
            vid_data = YouTube(vid_id=vid_id).get_video()
            video_title = vid_data["title"]
            video_id = vid_data["id"]
            video = LogMultimedia.objects.filter(video_id=video_id).first()
            description= "Hay nuevos comentarios en " + video_title
            admin = video.user if video else None
            new_notification= Notifications(user=request.user, description=description, admin=admin)
            new_notification.save()
            

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

        return render(request, 'infografias/detallesInfografias.html', context)

    def post(self, request, id):
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid() and request.user.is_authenticated:
            text = comment_form.cleaned_data['text']
        
            new_comment = CommentInfo(user=request.user, info_id_id=id, text=text)
            new_comment.save()
            infografia = Infographics.objects.filter(id=id).first()
            description= "Hay nuevos comentarios en " + infografia.title
            admin= infografia.user
            new_notification= Notifications(user=request.user, description=description, admin=admin)
            new_notification.save()
            return redirect(reverse('detallesInfografia', kwargs={'id': id}))

        return redirect('detallesInfografia', id=id)


class ReplyCommentInfo(View):
    def post(self, request, id, comment_id):
        comment = get_object_or_404(CommentInfo, id=comment_id)

        reply_form = CommentForm(request.POST)

        if reply_form.is_valid() and request.user.is_authenticated:
            text = reply_form.cleaned_data['text']

            new_reply = CommentInfo(user=request.user, info_id_id=id, text=text, parent_comment=comment)
            new_reply.save()
            infografia = Infographics.objects.filter(id=id).first()
            description= "Hay nuevos comentarios en " + infografia.title
            admin= infografia.user
            new_notification= Notifications(user=request.user, description=description, admin=admin)
            new_notification.save()
       
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
                messages.success(request, '¡Bienvenido a PuertoNet!')
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
            allowed_extensions = ['.mp4', '.avi', '.mkv']
            _, file_extension = os.path.splitext(file.name)
            if file_extension.lower() not in allowed_extensions:
                return False
            video_content = file.read()
            return True
    except Exception as e:
        print(f"Error al validar el video: {e}")
        return False




def subirContenido(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            form = LogImagenForm(request.POST, request.FILES)
        elif 'video_id' in request.POST:
            form = LogVideoForm(request.POST)
        else:
            # Manejar el caso en que no se proporcione un formulario válido
            return render(request, 'perfil/subirContenido/subirContenido.html')

        if form.is_valid():
            multimedia_instance = form.save(commit=False)


            if 'file' in request.FILES:
                # Es un formulario de imagen
                if not is_valid_image(form.cleaned_data['file']):
                    messages.error(request, 'El archivo no es una imagen válida.')
                    return render(request, 'perfil/subirContenido/subirContenido.html', {'form': form})

                infographics_instance = Infographics(
                    user=User.objects.get(id=request.user.id),
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    file=form.cleaned_data['file'],
                    category=form.cleaned_data['category'],
                )
                infographics_instance.save()


            elif 'video_id' in request.POST:
                # Es un formulario de video
                videos_instance = LogMultimedia(
                    user=User.objects.get(id=request.user.id),
                    title=form.cleaned_data['title'],
                    video_id=form.cleaned_data['video_id'],
                    category=form.cleaned_data['category'],
                )
                videos_instance.save()




            supplementary_videos = form.cleaned_data['supplementary_videos']
            supplementary_Infographics = form.cleaned_data['supplementary_Infographics']
            supplementary_Blogs = form.cleaned_data['supplementary_Blogs']

            if 'file' in request.FILES:
                infographics_instance.supplementary_videos.set(supplementary_videos)
                infographics_instance.supplementary_Infographics.set(supplementary_Infographics)
                infographics_instance.supplementary_Blogs.set(supplementary_Blogs)
                infographics_instance.save() 


            elif 'video_id' in request.POST:
                videos_instance.supplementary_videos.set(supplementary_videos)
                videos_instance.supplementary_Infographics.set(supplementary_Infographics)
                videos_instance.supplementary_Blogs.set(supplementary_Blogs)
                videos_instance.save() 



            messages.success(request, 'Se creó el contenido correctamente')
            return redirect('subirContenido')

    else:
        # Renderizar el formulario adecuado según la URL o cualquier otro criterio
        form1 = LogImagenForm()
        form2 = LogVideoForm()
        
        return render(request, 'perfil/subirContenido/subirContenido.html', {'form1': form1, 'form2': form2})

    return render(request, 'perfil/subirContenido/subirContenido.html', {'form1': form1, 'form2': form2})

    
def subirImagen(request):
    if request.method == 'POST':
        form = LogImagenForm(request.POST, request.FILES)
        if form.is_valid():
            multimedia_instance = form.save(commit=False)
            file = form.cleaned_data['file']
            if not is_valid_image(file):
                    messages.error(request, 'El archivo no es una imagen válida.')
                    return render(request, 'perfil/subirVideoImagen/subirImagen.html', {'form': form})
              
                # Guarda la información en Infographics
            infographics_instance = Infographics(
                    user=User.objects.get(id=request.user.id),
                    title= form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    file=form.cleaned_data['file'],
                    category=form.cleaned_data['category'],
                   
                )
            infographics_instance.save()

            supplementary_videos = form.cleaned_data['supplementary_videos']
            supplementary_Infographics = form.cleaned_data['supplementary_Infographics']
            supplementary_Blogs = form.cleaned_data['supplementary_Blogs']
                
            infographics_instance.supplementary_videos.set(supplementary_videos)
            infographics_instance.supplementary_Infographics.set(supplementary_Infographics)
            infographics_instance.supplementary_Blogs.set(supplementary_Blogs)
            infographics_instance.save() 

            messages.success(request, 'Se creo el contenido correctamente')
            return redirect('subirImagen')  
    else:
       form = LogImagenForm(request.POST, request.FILES)
    
    return render(request, 'perfil/subirVideoImagen/subirImagen.html', {'form': form})



def subirVideo(request):
    if request.method == 'POST':
        form = LogVideoForm(request.POST)
        if form.is_valid():
            multimedia_instance = form.save(commit=False)
            videos_instance = LogMultimedia(
                    user=User.objects.get(id=request.user.id),
                    title= form.cleaned_data['title'],
                    video_id=form.cleaned_data['video_id'],

                   
                )
            videos_instance.save()
            supplementary_videos = form.cleaned_data['supplementary_videos']
            supplementary_Infographics = form.cleaned_data['supplementary_Infographics']
            supplementary_Blogs = form.cleaned_data['supplementary_Blogs']
            videos_instance.supplementary_videos.set(supplementary_videos)
            videos_instance.supplementary_Infographics.set(supplementary_Infographics)
            videos_instance.supplementary_Blogs.set(supplementary_Blogs)
            videos_instance.save() 

            messages.success(request, 'Se creo el contenido correctamente')
            return redirect('subirVideo')  
    else:
       form = LogVideoForm(request.POST)
    return render(request, 'perfil/subirVideoImagen/subirVideo.html', {'form': form})

    
    


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

    return render(request, 'perfil/subirBlog/subirBlog.html', {'form': form, 'datos': blogs})

def editarBlog(request, id):
    blog = Blogs.objects.get(id=id)
    usuario_autenticado = request.user

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            # Actualiza los campos del blog existente con los datos del formulario
            form.save()

            messages.success(request, "Blog actualizado exitosamente.")
            return redirect('subirBlog')  # Ajusta según tu aplicación
        else:
            print(form.errors)
            messages.error(request, "Error al actualizar el blog. Verifica los datos.")
    else:
        # Pasa la instancia del blog al formulario para prellenar los campos existentes
        form = BlogForm(instance=blog)

    return render(request, 'perfil/subirBlog/editarBlog.html', {'form': form, 'datos': blog})



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
@login_required
def administrarContenido(request):
    infografias=Infographics.objects.all()
    videos=LogMultimedia.objects.all()
    blogs=Blogs.objects.all()
    
    context = {'infografias': infografias, 'videos':videos, 'blogs':blogs}
    return render(request, 'perfil/administrarContenido/administrarContenido.html',context)

@login_required
def EliminarInfografia(request, id):
    infografia = Infographics.objects.filter(id=id)
    infografia.delete()
    messages.success(request, "Eliminada correctamente")
    return redirect('administrarContenido')

@login_required
def EliminarVideo(request, id):
    video = LogMultimedia.objects.filter(id=id)
    video.delete()
    messages.success(request, "Registro eliminado correctamente")
    return redirect('administrarContenido')

@login_required
def EliminarBlog(request, id):
    Blog = Blogs.objects.filter(id=id)
    Blog.delete()
    messages.success(request, "Blog eliminado correctamente")
    return redirect('administrarContenido')

def notificaciones(request):
    notificaciones=Notifications.objects.filter(admin = request.user)
    context = {'notificaciones': notificaciones}
    return render(request, 'perfil/notificaciones/notificaciones.html', context)

@login_required
def vaciarNotificaciones(request):
    notificaciones = Notifications.objects.filter(admin=request.user)
    notificaciones.delete()
    messages.success(request, "Eliminadas correctamente")
    return redirect('notificaciones')




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
    return render(request, 'infografias/infografias.html', context)

