from django.contrib import admin
from apps.trabajadores.models import Trabajador, Sector
from apps.empresas.models import Empresa
from apps.usuarios.models import Usuario
from apps.beneficios.models import Beneficio, TipoBeneficio,ElementoBeneficio
# Register your models here.

class UAdmin(admin.ModelAdmin):
      pass
admin.site.register(Trabajador, UAdmin)
admin.site.register(Sector, UAdmin)
admin.site.register(Empresa, UAdmin)
admin.site.register(Usuario, UAdmin)
admin.site.register(Beneficio, UAdmin)
admin.site.register(TipoBeneficio, UAdmin)
admin.site.register(ElementoBeneficio, UAdmin)