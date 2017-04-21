from django.db import models
from django.contrib.auth.models import user


class Usuario(models.Model):
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=25)
    usuario = models.OneToOneField(User)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

        
