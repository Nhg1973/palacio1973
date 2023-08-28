
from django.contrib import admin
from django.urls import include, path
from publica.urls import *
from recetas.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('publica.urls')),
    path('', include('recetas.urls'))
]
