from django.db import models

# Create your models here.
class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    logo = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.nombre