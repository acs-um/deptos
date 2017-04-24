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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('titulo', models.CharField(verbose_name='Título', max_length=50)),
                ('descripción', models.CharField(verbose_name='Descripción', max_length=255)),
                ('categorias', models.CharField(verbose_name='Categorías', max_length=25)),
                ('precio', models.FloatField(verbose_name='Precio')),
                ('propietario', models.ForeignKey(to='usuarios.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('imagen', models.ImageField(verbose_name='Imagen', upload_to='fotos')),
                ('departamento', models.ForeignKey(verbose_name='departamento', related_name='fotos', to='departamentos.Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('texto', models.CharField(max_length=255)),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('departamento', models.ForeignKey(to='departamentos.Departamento')),
                ('usario_receptor', models.ForeignKey(related_name='mensajes_recibidos', to='usuarios.Usuario')),
                ('usuario_emisor', models.ForeignKey(related_name='mensajes_enviados', to='usuarios.Usuario')),
            ],
        ),
    ]
