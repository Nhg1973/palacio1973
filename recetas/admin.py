# admin.py

from django.contrib import admin
from .models import Receta, Ingrediente, IngredienteReceta, PasoReceta

# Define el administrador para el modelo IngredienteReceta
class IngredienteRecetaAdmin(admin.TabularInline):
    model = IngredienteReceta

# Define el administrador para el modelo PasoReceta
class PasoRecetaAdmin(admin.TabularInline):
    model = PasoReceta

# Define el administrador personalizado para el modelo Receta
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tiempo_preparacion', 'porciones')  # Campos a mostrar en la lista de Recetas
    list_filter = ('categoria',)  # Campos para filtrar las Recetas en el panel de administración
    search_fields = ('titulo', 'descripcion')  # Campos para realizar búsquedas en el panel de administración
    inlines = [IngredienteRecetaAdmin, PasoRecetaAdmin]  # Agrega los modelos en línea al formulario de Receta

# Registra los modelos con sus respectivos administradores personalizados
admin.site.register(Receta, RecetaAdmin)
admin.site.register(Ingrediente)
admin.site.register(IngredienteReceta)

