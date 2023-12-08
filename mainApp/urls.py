from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainApp.views import *
from . import views

urlpatterns = [
    path('', inicio.as_view(), name="inicio"),
    path('Inicio',inicio.as_view(),name='inicio'),
    path('Cursos',cursos.as_view(),name='Cursos'),
    path('Historia',historia.as_view(),name='Historia'),
    path('AvisoDePrivacidad',avisoprivacidad.as_view(),name='AvisoDePrivacidad'),
    path('TerminosYcondiciones',terminoscondiciones.as_view(),name='TerminosYcondiciones'),
	# path('play-video', views.play_video, name="play-video"),
    path('accounts/',include ('allauth.urls')),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('play-video/<str:vid_id>/', play_video.as_view(), name='play-video'),
    path('reply-comment/<str:vid_id>/<int:comment_id>/', ReplyComment.as_view(), name='reply-comment'),
    path('conocenos/', views.conocenos, name='Conocenos'),
    path('ComentarioPagina/', views.comentarioPagina, name='ComentarioPagina'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
