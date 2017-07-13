from django.db import models
from usuarios.models import Usuario
from django.utils import timezone


class Departamento(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    latitud = models.FloatField(default=0)
    longitud = models.FloatField(default=0)
    capacidad = models.IntegerField(default=0)
    localidad = models.CharField(max_length=50)
    precio = models.FloatField(default=0)
    usuario = models.ForeignKey(Usuario)

    def __str__(self):
        return  self.titulo

class Foto(models.Model):
    departamento = models.ForeignKey(Departamento)
    imagen = models.ImageField(upload_to='fotos')

    def __str__(self):
        return  self.departamento

class Comentario(models.Model):
    texto = models.CharField(max_length=255)
    emisor = models.ForeignKey(Usuario , related_name="comentario_enviados")
    fecha_envio = models.DateTimeField(auto_now_add=False);
    departamento = models.ForeignKey(Departamento)

    def __str__(self):
        return  self.texto
