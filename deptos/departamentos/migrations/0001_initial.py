# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('texto', models.CharField(max_length=255)),
                ('fecha_envio', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
                ('latitud', models.FloatField(default=0)),
                ('longitud', models.FloatField(default=0)),
                ('capacidad', models.IntegerField(default=0)),
                ('localidad', models.CharField(max_length=50)),
                ('precio', models.FloatField(default=0)),
                ('usuario', models.ForeignKey(to='usuarios.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('imagen', models.ImageField(upload_to='fotos')),
                ('departamento', models.ForeignKey(to='departamentos.Departamento')),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='departamento',
            field=models.ForeignKey(to='departamentos.Departamento'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='emisor',
            field=models.ForeignKey(related_name='comentario_enviados', to='usuarios.Usuario'),
        ),
    ]
