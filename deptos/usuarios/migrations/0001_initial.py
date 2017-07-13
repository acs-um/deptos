# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('texto', models.CharField(max_length=255)),
                ('fecha_envio', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('direccion', models.CharField(max_length=100, blank=True, null=True)),
                ('telefono', models.CharField(max_length=25, blank=True, null=True)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mensaje',
            name='emisor',
            field=models.ForeignKey(related_name='mensajes_enviados', to='usuarios.Usuario'),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='receptor',
            field=models.ForeignKey(related_name='mensajes_recibidos', to='usuarios.Usuario'),
        ),
    ]
