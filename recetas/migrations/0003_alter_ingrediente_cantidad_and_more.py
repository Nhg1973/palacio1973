# Generated by Django 4.2.3 on 2023-07-31 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_rename_fecha_actualizacion_ingrediente_fecha_actualizacion_mercado_central_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingrediente',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='ingrediente',
            name='valor_supermercado',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='ingrediente',
            name='valor_verduleria',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]