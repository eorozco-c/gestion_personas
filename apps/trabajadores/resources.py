from import_export import resources, widgets
from import_export.fields import Field
from .models import Trabajador

class TrabajadorExportResource(resources.ModelResource):
    sector = Field(attribute='sector__nombre',column_name='sector')
    created_at = Field(attribute='created_at',column_name='creado',widget=widgets.DateWidget('%d-%m-%Y %H:%M'))

    class Meta:
        model = Trabajador
        fields = ('id', 'nombre', 'apellido', 'email','rut','fecha_nacimiento','genero')
        export_order = ('id', 'nombre', 'apellido', 'email','rut','fecha_nacimiento','genero','sector','created_at',)
        skip_unchanged = True
        report_skipped = False
        dry_run = True
    
    def dehydrate_genero(self, Trabajador):
        genero = Trabajador.genero
        if genero == 1:
            genero = "F"
        elif genero == 2:
            genero = "M"
        else:
            genero = "O"
        return genero