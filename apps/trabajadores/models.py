from apps.beneficios.models import Beneficio, ElementoBeneficio
from django.db import models
from ..empresas.models import Empresa
# Create your models here.

class Sector(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=150)
    empresa = models.ForeignKey(Empresa, related_name="sector_empresa", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.nombre

class Trabajador(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    rut = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    genero = models.PositiveIntegerField(default=1)
    empresa = models.ForeignKey(Empresa, related_name="trabajador_empresa", on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, related_name="trabajador_sector", on_delete=models.PROTECT)
    beneficio = models.ManyToManyField(Beneficio, through="TrabajadorBeneficio")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TrabajadorBeneficio(models.Model):
    trabajador = models.ForeignKey(Trabajador, related_name="beneficio_trabajador", on_delete=models.CASCADE)
    beneficio = models.ForeignKey(Beneficio, related_name="trabajador_beneficio", on_delete=models.CASCADE)
    elemento = models.ForeignKey(ElementoBeneficio, related_name="beneficio_trabajador_elemento", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)