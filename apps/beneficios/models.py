from django.db import models
from ..empresas.models import Empresa
# Create your models here.
class  TipoBeneficio(models.Model):
    nombre = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, related_name="tipo_beneficios_empresa", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.nombre

class Beneficio(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    empresa = models.ForeignKey(Empresa, related_name="beneficios_empresa", on_delete=models.CASCADE)
    tipo_beneficio = models.ForeignKey(TipoBeneficio, related_name="beneficios_tipo", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ElementoBeneficio(models.Model):
    nombre = models.CharField(max_length=50)
    beneficio = models.ForeignKey(Beneficio, related_name="beneficios_elemento", on_delete=models.CASCADE)

