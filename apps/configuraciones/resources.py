from apps.documentos.models import TipoDocumento
from import_export import resources, widgets
from import_export.fields import Field
from apps.trabajadores.models import Sector
from apps.beneficios.models import TipoBeneficio

class SectorExportResource(resources.ModelResource):
    created_at = Field(attribute='created_at',column_name='creado',widget=widgets.DateWidget('%d-%m-%Y %H:%M'))

    class Meta:
        model = Sector
        fields = ('id', 'nombre', 'direccion',)
        export_order = ('id', 'nombre', 'direccion','created_at',)
        skip_unchanged = True
        report_skipped = False
        dry_run = True
    
class TipoBeneficioExportResource(resources.ModelResource):
    created_at = Field(attribute='created_at',column_name='creado',widget=widgets.DateWidget('%d-%m-%Y %H:%M'))

    class Meta:
        model = TipoBeneficio
        fields = ('id', 'nombre',)
        export_order = ('id', 'nombre','created_at',)
        skip_unchanged = True
        report_skipped = False
        dry_run = True
    
class TipoDocumentoExportResource(resources.ModelResource):
    created_at = Field(attribute='created_at',column_name='creado',widget=widgets.DateWidget('%d-%m-%Y %H:%M'))

    class Meta:
        model = TipoDocumento
        fields = ('id', 'nombre',)
        export_order = ('id', 'nombre','created_at',)
        skip_unchanged = True
        report_skipped = False
        dry_run = True