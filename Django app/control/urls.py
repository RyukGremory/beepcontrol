from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('locks', views.locksView, name='locksView'),
    path('control', views.controlView, name='controlView'),
    path('registro', views.registroView, name='registroView'),
    
]