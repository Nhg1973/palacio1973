# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Ingrediente
import json

def cargar_json(request):
    if request.method == 'POST':
        # Procesar el JSON recibido en el request.POST o request.FILES
        data = json.loads(request.POST.get('json_data'))  # Aquí se convierte el JSON a un diccionario Python
        fuente = 'mercado_central'  # O 'productos', según corresponda a tu caso.
        resultado = Ingrediente.cargar_desde_json(data, fuente)
        return JsonResponse({'resultado': 'Datos cargados exitosamente'})

    return render(request, 'cargar_json.html')
