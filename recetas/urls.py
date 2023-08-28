# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Otras URLs de la aplicación
    # ...
    path('cargar_json/', views.cargar_json, name='cargar_json'),
]
