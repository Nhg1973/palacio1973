from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('',home, name='home'),
    path('comidas',comidas, name='comidas'),
    path('obtener_receta/<int:receta_id>/', obtener_receta, name='obtener_receta'),
    path('calcular_ingredientes/', calcular_lista_ingredientes, name='calcular_lista_ingredientes'),
]