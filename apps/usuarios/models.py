from django.db import models
from ..empresas.models import Empresa

# Create your models here.
class Perfil(models.Model):
    nombre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    rut = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    genero = models.PositiveIntegerField(default=1)
    password = models.CharField(max_length=255)
    perfil = models.ForeignKey(Perfil, related_name="usuario_perfil", on_delete=models.PROTECT)
    empresa = models.ForeignKey(Empresa, related_name="usuario_empresa", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

