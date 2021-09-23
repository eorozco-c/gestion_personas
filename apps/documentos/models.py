from django.db import models
from ..empresas.models import Empresa
from ..trabajadores.models import Trabajador
from ..beneficios.models import Beneficio

# Create your models here.
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50)
    empresa = models.ForeignKey(Empresa, related_name="tipo_documento_empresa",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        for field_name in ['nombre']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(TipoDocumento, self).save(*args, **kwargs)

class DocumentoTrabajador(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.TextField(blank=True,null=True)
    tipo_documento = models.ForeignKey(TipoDocumento, related_name="documento_trabajador_tipo", on_delete=models.PROTECT)
    trabajador = models.ForeignKey(Trabajador, related_name="documento_trabajador", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DocumentoBeneficio(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.TextField(blank=True,null=True)
    tipo_documento = models.ForeignKey(TipoDocumento, related_name="documento_beneficio_tipo", on_delete=models.PROTECT)
    beneficio = models.ForeignKey(Beneficio, related_name="documento_beneficio", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

