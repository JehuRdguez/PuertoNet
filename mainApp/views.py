from django.shortcuts import redirect, render
from django.views import View
from .mixins import YouTube
from django.contrib.auth import  logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm,CommentForm
from .models import Comment, ComentariosPagina
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from itertools import chain

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
     
class cursos(View):
    def get(self, request):
        videos = YouTube().get_data()

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
        
        context = {"videos": videos_pagina, "unique_categories": unique_categories}
        return render(request, 'cursos/cursos.html', context)
    
def ordenar_videos(request):
    opcion = request.GET.get('opcion', 'AgregadosRecientemente')
    categoria = request.GET.get('categoria', 'Todos')

    # Lógica de ordenación según la opción y la categoría
    videos = Video.objects.all()

    if categoria != 'Todos':
        videos = videos.filter(categoria__nombre=categoria)

    if opcion == 'AgregadosRecientemente':
        videos = videos.order_by('-fecha_agregado')
    elif opcion == 'Alfabeticamente':
        videos = videos.order_by('titulo')

    # Renderiza la lista de videos ordenada y devuélvela como JSON
    data = render(request, 'cursos/lista_videos.html', {'videos': videos})
    return JsonResponse({'html': data.content})


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

 