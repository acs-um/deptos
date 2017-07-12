from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    usuario = models.OneToOneField(User)

    def __str__(self):
        return '%s %s' % (self.usuario.first_name, self.usuario.last_name)

class Mensaje(models.Model):
    texto = models.CharField(max_length=255)
    emisor = models.ForeignKey(Usuario , related_name="mensajes_enviados")
    receptor = models.ForeignKey(Usuario , related_name="mensajes_recibidos")
    fecha_envio = models.DateTimeField(auto_now_add=False);

    def __str__(self):
        return  self.texto
