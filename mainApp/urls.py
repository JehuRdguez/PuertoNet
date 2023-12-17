from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainApp.views import *
from . import views

urlpatterns = [
    path('', inicio.as_view(), name="inicio"),
    path('Inicio',inicio.as_view(),name='inicio'),
    path('Blogs',Blogs.as_view(),name='Blogs'),
    path('Cursos',cursos.as_view(),name='Cursos'),
    path('cursosOrden',cursosOrden.as_view(),name='cursosOrden'),
    path('Historia',historia.as_view(),name='Historia'),
    path('AvisoDePrivacidad',avisoprivacidad.as_view(),name='AvisoDePrivacidad'),
    path('TerminosYcondiciones',terminoscondiciones.as_view(),name='TerminosYcondiciones'),
    path('Soporte',soporte.as_view(),name='Soporte'),
	# path('play-video', views.play_video, name="play-video"),
    path('accounts/',include ('allauth.urls')),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('play-video/<str:vid_id>/', play_video.as_view(), name='play-video'),
    path('reply-comment/<str:vid_id>/<int:comment_id>/', ReplyComment.as_view(), name='reply-comment'),
    path('conocenos/', views.conocenos, name='Conocenos'),
    path('ComentarioPagina/', views.comentarioPagina, name='ComentarioPagina'),
    path('editarUsuario/', views.editarUsuario, name='editarUsuario'),
    path('subirVideoImagen/', views.subirVideoImagen, name='subirVideoImagen'),
    path('subirBlog/', views.subirBlog, name='subirBlog'),
    path('administrarContenido/', views.administrarContenido, name='administrarContenido'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
