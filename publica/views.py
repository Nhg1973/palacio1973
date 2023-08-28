from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from recetas.models import Receta, Ingrediente, IngredienteReceta
from django.views.decorators.http import require_POST
from decimal import Decimal
from collections import defaultdict
from unidecode import unidecode
import logging


def home(request):

    titulo = 'Pública'
    context = {
     #contexto 
    }
    print(context)
    return render(request, 'gestion_publica/home/index.html', context)

def comidas(request):
    recetas = Receta.objects.all()

    context = {
        'recetas': recetas,
    }

    return render(request, 'gestion_publica/home/comidas.html', context)




# Configura el sistema de registro
logger = logging.getLogger(__name__)

# ... (código previo)

@csrf_exempt
@require_POST
def calcular_lista_ingredientes(request):
    recetas_seleccionadas = request.POST.getlist('recetas[]')
    cantidad_personas = int(request.POST.get('cantidad_personas'))
    cantidad_personas_decimal = Decimal(cantidad_personas)

    hortalizasYFrutasChico = [
        { 'nombre': "Azucar", 'cantidad_caja': 12 },
        { 'nombre': "Berenjenas", 'cantidad_caja': 12 },
        { 'nombre': "Caldo", 'cantidad_caja': 12 },
        { 'nombre': "Duraznos", 'cantidad_caja': 12 },
        { 'nombre': "Frutillas", 'cantidad_caja': 12 },

    ]  

    hortalizasYFrutas = [
        { 'nombre': "Azucar", 'cantidad_caja': 24},
        { 'nombre': "Berenjenas", 'cantidad_caja': 24},
        { 'nombre': "Caldo", 'cantidad_caja': 24 },
        { 'nombre': "Duraznos", 'cantidad_caja': 24},
        { 'nombre': "Frutillas", 'cantidad_caja': 24 },

    ]   

    hortalizasYFrutasGrande = [
        { 'nombre': "Azucar", 'cantidad_caja': 36 },
        { 'nombre': "Berenjenas", 'cantidad_caja': 36 },
        { 'nombre': "Caldo", 'cantidad_caja': 36 },
        { 'nombre': "Duraznos", 'cantidad_caja': 36 },
        { 'nombre': "Frutillas", 'cantidad_caja': 36},

    ]  


    lista_ingredientes = ListaIngredientes()

    for receta_id in recetas_seleccionadas:
        ingredientes_receta = IngredienteReceta.objects.filter(receta_id=receta_id)
        
        for ingrediente_receta in ingredientes_receta:
            cantidad_ajustada_decimal = (ingrediente_receta.cantidad * cantidad_personas_decimal) / Decimal(ingrediente_receta.receta.porciones)
            cantidad_ajustada_float = float(cantidad_ajustada_decimal)
            valor_ingrediente = ingrediente_receta.ingrediente.media_prom_pk
            lista_ingredientes.agregar_ingrediente(
                ingrediente_receta.ingrediente.nombre,
                cantidad_ajustada_float,
                valor_ingrediente
            )

    resultado_lista = lista_ingredientes.obtener_lista()
    #print("Resultado listar",resultado_lista)

    diferencia_chico = calcular_diferencia(resultado_lista, hortalizasYFrutasChico)
    diferencia_mediano = calcular_diferencia(resultado_lista, hortalizasYFrutas)
    diferencia_grande = calcular_diferencia(resultado_lista, hortalizasYFrutasGrande)

    opciones = {
        'Chico': diferencia_chico,
        'Mediano': diferencia_mediano,
        'Grande': diferencia_grande
    }

    # Después de calcular la opción más cercana
    opcion_mas_cercana = min(opciones, key=opciones.get)
    #print("La opción más cercana es:", opcion_mas_cercana)

    info_adicional = {
    'cajon_tipo': opcion_mas_cercana,
    'otro_valor_relevante': "valor aquí"  # Cambia esto por el valor que necesitas
    }

    # Obtener los ingredientes de la opción más cercana
    if opcion_mas_cercana == 'Chico':
        ingredientes_opcion = hortalizasYFrutasChico
    elif opcion_mas_cercana == 'Mediano':
        ingredientes_opcion = hortalizasYFrutas
    else:
        ingredientes_opcion = hortalizasYFrutasGrande

    #print("Ingredientes de la opción más cercana asignados a resultado_lista:", resultado_lista)

    ingredientes_coincidentes = {nombre for nombre, _ in resultado_lista}
    #print("Ingredientes coincidencuia",ingredientes_coincidentes)
    ingredientes_faltantes = [item for item in ingredientes_opcion if unidecode(item['nombre'].upper()) not in ingredientes_coincidentes]
    #print("Ingredientes faltantes",ingredientes_faltantes)
    resultado_serializable = [
        {
            'nombre': item['nombre'],
            'tipo': 3,  # Por defecto, no está en ingredientes ni en hortalizasYFrutas
            'cantidad_ajustada': None,
            'valor': None,
            'cantidad_caja': item['cantidad_caja'],
            'producto': 0
        }
        for item in ingredientes_faltantes
    ]

    suma_total_tipo1 = 0  # Inicializar la suma total de cantidades tipo 1
    suma_total_tipo2 = 0 
    suma_total_tipo3 = 0 
   
    for nombre, datos in resultado_lista:
        item_encontrado = next((item for item in hortalizasYFrutas if unidecode(item['nombre'].strip().upper()) == unidecode(nombre.strip().upper())), None)
        #tipo = 2  # Por defecto, coincide con ingredientes pero no con hortalizasYFrutas
        
        if nombre in ingredientes_coincidentes and item_encontrado:
            tipo = 1  # Coincide con ingredientes y con hortalizasYFrutas
            suma_total_tipo1 += datos['cantidad']  # Sumar la cantidad ajustada si es tipo 1
        
            
        elif nombre in ingredientes_coincidentes:
            tipo = 2  # Coincide con ingredientes pero no con hortalizasYFrutas
            suma_total_tipo2 += datos['cantidad']  # Sumar la cantidad ajustada si es tipo 1
        
            
        elif nombre in item_encontrado:
            tipo = 3  # Está en hortalizasYFrutas solamente
            suma_total_tipo3 += datos['cantidad']  # Sumar la cantidad ajustada si es tipo 1
        
        
        resultado_serializable.append({
            'nombre': nombre,
            'tipo': tipo,
            'cantidad_ajustada': datos['cantidad'],
            'valor': datos['valor'],
            'cantidad_caja': item_encontrado['cantidad_caja'] if item_encontrado else None,
            'producto': datos['cantidad'] * datos['valor'] if datos['cantidad'] is not None and datos['valor'] is not None else 0
        })

        for ingrediente in resultado_serializable:
            ingrediente.update(info_adicional)

    #suma_total = suma_total_tipo1 + suma_total_tipo2 +suma_total_tipo3
    #print("Suma cantidad coincide con la oferta: ",suma_total_tipo1)
    #print("Suma cantidad que no coincide con la oferta: ",suma_total_tipo2)
    #print("Suma cantidad se ofrece pero que no se solicita: ",suma_total_tipo3)
    #print("Suma cantidad total : ",suma_total)


    return JsonResponse({'ingredientes': resultado_serializable})


def obtener_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    # Devuelve los detalles de la receta en formato JSON
    data = {
        "titulo": receta.titulo,
        "descripcion": receta.descripcion,
        "imagen_url": receta.imagen.url if receta.imagen else None,  # Agrega la URL de la imagen si 
        # Agrega aquí otros campos que necesitas
    }
    return JsonResponse(data)

class ListaIngredientes:
    def __init__(self):
        self.ingredientes = defaultdict(lambda: {'cantidad': 0, 'valor': 0})
    
    def agregar_ingrediente(self, ingrediente, cantidad, valor):
        self.ingredientes[ingrediente]['cantidad'] += cantidad
        self.ingredientes[ingrediente]['valor'] = valor
    
    def obtener_lista(self):
        return [(nombre, datos) for nombre, datos in self.ingredientes.items()]
    
def calcular_diferencia(lista_generada, opcion):
    diferencia_total = 0
    
    for ingrediente_lista_generada in lista_generada:
        nombre_ingrediente = ingrediente_lista_generada['nombre']
        cantidad_ingrediente_lista_generada = ingrediente_lista_generada['cantidad']
        
        for ingrediente_opcion in opcion:
            if ingrediente_opcion['nombre'] == nombre_ingrediente:
                cantidad_ingrediente_opcion = ingrediente_opcion['cantidad_caja']
                diferencia = abs(cantidad_ingrediente_lista_generada - cantidad_ingrediente_opcion)
                diferencia_total += diferencia
                break
    
    return diferencia_total

def calcular_diferencia(lista_generada, opcion):
        diferencia_total = 0
        
        for ingrediente_lista_generada in lista_generada:
            nombre_ingrediente = ingrediente_lista_generada[0]
            cantidad_ingrediente_lista_generada = ingrediente_lista_generada[1]['cantidad']
            
            for ingrediente_opcion in opcion:
                if ingrediente_opcion['nombre'] == nombre_ingrediente:
                    cantidad_ingrediente_opcion = ingrediente_opcion['cantidad_caja']
                    diferencia = abs(cantidad_ingrediente_lista_generada - cantidad_ingrediente_opcion)
                    diferencia_total += diferencia
                    break
        
        return diferencia_total





