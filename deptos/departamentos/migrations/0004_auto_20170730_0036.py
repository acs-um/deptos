# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('departamentos', '0003_auto_20170723_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='capacidad',
            field=models.IntegerField(choices=[(1, 'Un estudiante'), (2, 'Dos estudiantes'), (3, 'Tres estudiantes'), (4, 'Cuatro estudiantes'), (5, 'Cinco estudiantes')], default=1),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='descripcion',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='localidad',
            field=models.CharField(max_length=25, choices=[('Mendoza (Capital)', 'Mendoza (Capital)'), ('General Alvear', 'General Alvear'), ('Godoy Cruz', 'Godoy Cruz'), ('Guaymallén', 'Guaymallén'), ('Junín', 'Junín'), ('La Paz', 'La Paz'), ('Las Heras', 'Las Heras'), ('Lavalle', 'Lavalle'), ('Luján de Cuyo', 'Luján de Cuyo'), ('Maipú', 'Maipú'), ('Malargüe', 'Malargüe'), ('Rivadavia', 'Rivadavia'), ('San Carlos', 'San Carlos'), ('San Martín', 'San Martín'), ('San Rafael', 'San Rafael'), ('Santa Rosa', 'Santa Rosa'), ('Tunuyán', 'Tunuyán'), ('Tupungato', 'Tupungato')]),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='precio',
            field=models.FloatField(),
        ),
    ]
