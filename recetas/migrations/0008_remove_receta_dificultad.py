# Generated by Django 4.2.3 on 2023-08-01 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0007_remove_receta_instrucciones_alter_receta_categoria_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receta',
            name='dificultad',
        ),
    ]
