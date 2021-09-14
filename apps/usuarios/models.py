from django.contrib.auth.models import AbstractUser
from django.db import models
from ..empresas.models import Empresa

# Create your models here.
class Perfil(models.Model):
    nombre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.nombre

class Usuario(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    rut = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    genero = models.PositiveIntegerField(default=1)
    perfil = models.ForeignKey(Perfil, related_name="usuario_perfil", on_delete=models.PROTECT)
    empresa = models.ForeignKey(Empresa, related_name="usuario_empresa", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        for field_name in ['first_name','last_name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Usuario, self).save(*args, **kwargs)