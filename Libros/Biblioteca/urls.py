from django.urls import path
from . import views

urlpatterns = [
    # Bibliotecas
    path('Biblioteca/', views.Lista_Biblioteca, name='Lista_Biblioteca'),
    path('Biblioteca/<int:id>/', views.Detalles_Biblioteca, name='Detalles_Biblioteca'),

    # Libros
    path('Libro/', views.Lista_Libro, name='Lista_Libro'),
    path('Libro/<int:id>/', views.Detalles_Libro, name='Detalles_Libro'),

    # Usuarios
    path('Usuario/', views.Lista_Usuario, name='Lista_Usuario'),
    path('Usuario/<int:id>/', views.Detalles_Usuario, name='Detalles_Usuario'),

    # Préstamos
    path('Prestamo/', views.Lista_Prestamo, name='Lista_Prestamo'),
    path('Prestamo/<int:id>/', views.Detalles_Prestamo, name='Detalles_Prestamo'),
]