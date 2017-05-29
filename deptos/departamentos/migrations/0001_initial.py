# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('titulo', models.CharField(max_length=50, verbose_name='Título')),
                ('descripción', models.CharField(max_length=255, verbose_name='Descripción')),
                ('categorias', models.CharField(max_length=25, verbose_name='Categorías')),
                ('precio', models.FloatField(verbose_name='Precio')),
                ('propietario', models.ForeignKey(to='usuarios.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('imagen', models.ImageField(upload_to='fotos', verbose_name='Imagen')),
                ('departamento', models.ForeignKey(to='departamentos.Departamento', related_name='fotos', verbose_name='departamento')),
            ],
        ),
    ]
