# Generated by Django 5.1.1 on 2024-11-06 23:27

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(unique=True)),
                ('descripcion', models.CharField(max_length=255)),
                ('categoria', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_vendida', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionApp.articulo')),
            ],
        ),
    ]
