from django.db import models
from usuarios.models import Usuario
from django.utils import timezone

LOCALIDAD = (
    ('Mendoza (Capital)', "Mendoza (Capital)"),
    ('General Alvear', "General Alvear"),
    ('Godoy Cruz', "Godoy Cruz"),
    ('Guaymallén', "Guaymallén"),
    ('Junín', "Junín"),
    ('La Paz', "La Paz"),
    ('Las Heras', "Las Heras"),
    ('Lavalle', "Lavalle"),
    ('Luján de Cuyo', "Luján de Cuyo"),
    ('Maipú', "Maipú"),
    ('Malargüe', "Malargüe"),
    ('Rivadavia', "Rivadavia"),
    ('San Carlos', "San Carlos"),
    ('San Martín', "San Martín"),
    ('San Rafael', "San Rafael"),
    ('Santa Rosa', "Santa Rosa"),
    ('Tunuyán', "Tunuyán"),
    ('Tupungato', "Tupungato"),
)

CAPACIDAD = (
    (1, "Un estudiante"),
    (2, "Dos estudiantes"),
    (3, "Tres estudiantes"),
    (4, "Cuatro estudiantes"),
    (5, "Cinco estudiantes"),
)

class Departamento(models.Model):
    titulo = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.CharField(max_length=400, blank=False, null=False)
    latitud = models.FloatField(default=0.0)
    longitud = models.FloatField(default=0.0)
    capacidad = models.IntegerField(default=1, null=False, choices=CAPACIDAD)
    localidad = models.CharField(max_length=25, null=False, choices=LOCALIDAD)
    precio = models.FloatField(null=False, blank=False)
    estado = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario)

    def __unicode__(self,):
        return self.titulo

class Foto(models.Model):
    departamento = models.ForeignKey(Departamento)
    imagen = models.ImageField(upload_to='fotos')

    def __str__(self):
        return '%s' % (self.departamento.titulo)

class Comentario(models.Model):
    texto = models.CharField(max_length=255)
    emisor = models.ForeignKey(Usuario , related_name="comentario_enviados")
    fecha_envio = models.DateTimeField(auto_now_add=False);
    departamento = models.ForeignKey(Departamento)

    def __str__(self):
        return  self.texto
