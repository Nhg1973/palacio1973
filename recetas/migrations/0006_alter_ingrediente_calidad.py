# Generated by Django 4.2.3 on 2023-07-31 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0005_remove_ingrediente_cantidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingrediente',
            name='calidad',
            field=models.CharField(max_length=10, null=True),
        ),
    ]