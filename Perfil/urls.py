from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio (Tu función se llama 'home')
    path('', views.home, name='home'),
    
    # Generador de CV
    path('cv-print/', views.vista_previa_cv, name='vista_previa_cv'),

    # Páginas de detalle (Las que usas en los botones "Ver más")
    path('experiencia/', views.experiencia, name='experiencia'),
    path('cursos/', views.cursos, name='cursos'),
    path('logros/', views.reconocimientos, name='reconocimientos'),
    path('academicos/', views.productos_academicos, name='productos_academicos'),
    path('proyectos/', views.productos_laborales, name='productos_laborales'),
    path('garage/', views.garage, name='garage'),
]