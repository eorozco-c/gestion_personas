from import_export import resources, widgets
from import_export.fields import Field
from .models import Beneficio

class BeneficioExportResource(resources.ModelResource):
    tipo_beneficio = Field(attribute='tipo_beneficio__nombre',column_name='tipo_beneficio')
    created_at = Field(attribute='created_at',column_name='creado',widget=widgets.DateWidget('%d-%m-%Y %H:%M'))

    class Meta:
        model = Beneficio
        fields = ('id', 'nombre', 'fecha_inicio', 'fecha_fin',)
        export_order = ('id', 'nombre', 'fecha_inicio', 'fecha_fin','tipo_beneficio','created_at',)
        skip_unchanged = True
        report_skipped = False
        dry_run = True
    