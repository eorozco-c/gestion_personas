from django.urls import  path
from . import views

app_name = "configuraciones"

urlpatterns = [
    path('', views.index, name="index"),
    path('sectores',views.NuevoSector.as_view(), name="sectores" ),
    path('sectores/edit/<int:pk>',views.EditSector.as_view(), name="sectores_edit"),
    path('sectores/predestroy/<int:pk>',views.sectores_predestroy, name="sectores_predestroy"),
    path('sectores/destroy/<int:pk>',views.sectores_destroy, name="sectores_destroy"),
    path('documentos',views.NuevoTipoDocumento.as_view(), name="documentos" ),
    path('documentos/edit/<int:pk>',views.EditTipoDocumento.as_view(), name="documentos_edit"),
    path('documentos/predestroy/<int:pk>',views.documentos_predestroy, name="documentos_predestroy"),
    path('documentos/destroy/<int:pk>',views.documentos_destroy, name="documentos_destroy"),
    path('beneficios',views.NuevoTipoBeneficio.as_view(), name="beneficios" ),
    path('beneficios/edit/<int:pk>',views.EditTipoBeneficio.as_view(), name="beneficios_edit"),
    path('beneficios/predestroy/<int:pk>',views.beneficios_predestroy, name="beneficios_predestroy"),
    path('beneficios/destroy/<int:pk>',views.beneficios_destroy, name="beneficios_destroy"),
    path('exportSector',views.SectorExport, name="exportSector"),
    path('exportTipoBeneficio',views.TipoBeneficioExport, name="exportTipoBeneficio"),
    path('exportTipoDocumento',views.TipoDocumentoExport, name="exportTipoDocumento"),
]
