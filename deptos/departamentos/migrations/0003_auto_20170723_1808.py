# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('departamentos', '0002_departamento_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='capacidad',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='localidad',
            field=models.CharField(max_length=25),
        ),
    ]
