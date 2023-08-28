import decimal
from django.db import models
from django.utils import timezone




class Ingrediente(models.Model):
    
    nombre = models.CharField(max_length=100)
    variedad = models.CharField(max_length=50,null=True)  # Permite valor nulo)
    procedencia = models.CharField(max_length=50,null=True)  # Permite valor nulo)
    envase = models.CharField(max_length=50,null=True)  # Permite valor nulo)
    calidad = models.CharField(max_length=10, null=True)  # Permite valor
    tamaño = models.CharField(max_length=50,null=True)  # Permite valor nulo)
    grado = models.CharField(max_length=50,null=True)  # Permite valor nulo)
    media_prom_pk = models.FloatField(null=True)  # Permitir valor nulo
    fecha_actualizacion_mercado_central = models.DateTimeField(default=timezone.now)
    fecha_actualizacion_productos = models.DateTimeField(default=timezone.now)    

    def __str__(self):
        return self.nombre
    @classmethod
    def cargar_desde_json(cls, data, fuente):
        for especie_key, especie_data in data.items():
            # Extraemos los valores necesarios del diccionario
            nombre = especie_data.get('Especie', cls._meta.get_field('nombre').get_default())
            variedad = especie_data.get('Variedad', None)  # Puede ser None si no se proporciona en el JSON
            procedencia = especie_data.get('Procedencia', None)  # Puede ser None si no se proporciona en el JSON
            envase = especie_data.get('Envase', None)  # Puede ser None si no se proporciona en el JSON
            calidad = especie_data.get('Calidad', None)
            tamaño = especie_data.get('Tamaño', None)  # Puede ser None si no se proporciona en el JSON
            grado = especie_data.get('Grado', None)  # Puede ser None si no se proporciona en el JSON
            
            mo = especie_data.get('Mo', 1)
            kg = especie_data.get('Kilos', 1)
            
            if kg != 0:
                media_prom_pk = mo / kg
            else:
                media_prom_pk = None  # O cualquier otro valor predeterminado en caso de división por cero

            try:
                ingrediente = cls.objects.get(nombre=nombre)
            except cls.DoesNotExist:
                # If the instance does not exist, create a new one
                ingrediente = cls(nombre=nombre)

            # Set the fields using **kwargs
            ingrediente.nombre = nombre
            ingrediente.variedad = variedad
            ingrediente.procedencia = procedencia
            ingrediente.envase = envase
            ingrediente.calidad = calidad
            ingrediente.tamaño = tamaño
            ingrediente.grado = grado
            ingrediente.media_prom_pk = media_prom_pk

            # Set the appropriate timestamp field based on the source
            if fuente == 'mercado_central':
                ingrediente.fecha_actualizacion_mercado_central = timezone.now()
            elif fuente == 'productos':
                ingrediente.fecha_actualizacion_productos = timezone.now()
            else:
                raise ValueError("Fuente inválida: debe ser 'mercado_central' o 'productos'")

            # Save the instance inside the loop
            ingrediente.save()

        # Return the last instance after the loop has finished
        return ingrediente


class Receta(models.Model):
    CATEGORIAS_OPCIONES = [
        ('TARTA', 'Tartas'),
        ('CARNES', 'Carnes'),
        ('SOPAS', 'Sopas'),
        # Agrega más opciones según sea necesario
    ]
    # Campos existentes
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    ingredientes = models.ManyToManyField(Ingrediente, through='IngredienteReceta')
    tiempo_preparacion = models.CharField(max_length=50)
    porciones = models.PositiveIntegerField()
    tiempo_coccion = models.CharField(max_length=50)
    categoria = models.CharField(max_length=100, choices=CATEGORIAS_OPCIONES)
    imagen = models.ImageField(upload_to='static/assets/img/recetas', null=True, blank=True)
    video = models.FileField(upload_to='static/assets/img/videos/', null=True, blank=True)
    enlace_video = models.URLField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class PasoReceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    paso = models.PositiveIntegerField()
    descripcion = models.TextField()

    def __str__(self):
        return f"Paso {self.paso}: {self.descripcion}"



class IngredienteReceta(models.Model):
    UNIDADES_DE_MEDIDA_OPCIONES = [
    ('gramo', 'gramo'),
    ('kilo', 'kilo'),
    ('mililitro', 'mililitro'),
    ('litro', 'litro'),
    ('taza', 'taza'),
    ('cucharadita', 'cucharadita'),
    ('cucharada', 'cucharada'),
    ('unidad', 'unidad'),
    ('unidades', 'unidades'),
    ('a gusto', 'a gusto'),
    ('paquete', 'paquete'),
    # Agrega más opciones según sea necesario
]

    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_de_medida = models.CharField(max_length=50, choices=UNIDADES_DE_MEDIDA_OPCIONES)
    cantidad_ajustada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        if self.cantidad_ajustada is not None:
            return f"{self.cantidad_ajustada} {self.unidad_de_medida} de {self.ingrediente.nombre} para {self.receta.titulo}"
        else:
            return f"{self.cantidad} {self.unidad_de_medida} de {self.ingrediente.nombre} para {self.receta.titulo}"
