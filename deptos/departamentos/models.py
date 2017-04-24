from django.db import models
from usuarios.models import Usuario



class Departamento(models.Model):
    titulo = models.CharField("Título", max_length=50)
    descripción = models.CharField("Descripción", max_length=255)
    ubicación = "ver como hacer con api maps"
    categorias = models.CharField("Categorías", max_length=25)
    precio = models.FloatField("Precio")
    propietario = models.ForeignKey(Usuario)

class Foto(models.Model):
    departamento = models.ForeignKey("Departamento", verbose_name="departamento", related_name="fotos")
    imagen = models.ImageField("Imagen", upload_to='fotos')


class Mensaje(models.Model):
    texto = models.CharField(max_length=255)
    usuario_emisor = models.ForeignKey(Usuario , related_name="mensajes_enviados")
    usario_receptor = models.ForeignKey(Usuario , related_name="mensajes_recibidos")
    fecha_envio = models.DateTimeField(auto_now_add=True)
    departamento = models.ForeignKey(Departamento)
