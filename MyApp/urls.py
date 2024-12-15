from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('intereses/', views.intereses, name='intereses'),
    path('blog/', views.blog, name='blog'),
    path('ejercicios/', views.ejercicios, name='ejercicios'),
    path('sort-data/', views.sort_data, name='sort_data'),
    path('generate-random-data/', views.generate_random_data_view, name='generate_random_data'),
    path('read-data/', views.read_data_view, name='read_data'),
    path('grafica/', views.grafica_view, name='grafica'),
    path('descargar/', views.descargar_view, name='descargar'),
    path('filtros/', views.filtros_view, name='filtros')
]
