from django.urls import  path
from . import views

app_name = "trabajadores"

urlpatterns = [
    path('', views.ListTrabajadores.as_view(), name="index"),
    path('new',views.CreateTrabajador.as_view(), name="new_worker"),
    path('view/<int:pk>',views.DetalleTrabajador.as_view(), name="detail_worker"),
    path('edit/<int:pk>',views.EditTrabajador.as_view(), name="edit"),
    path('predestroy/<int:pk>',views.predestroy, name="predestroy"),
    path('destroy/<int:pk>',views.destroy, name="destroy"),
    path('export',views.TrabajadorExport, name="export"),
    path('import',views.TrabajadorImport, name="import"),
    path('cargaDoc/<int:pk>',views.CargaDocumento, name="cargaDoc"),
    path('descargaDoc/<int:pk>',views.DescargaDocumento, name="descargaDoc"),
    path('obtieneElementos/<int:pk>',views.ElementosBeneficio, name="obtieneElementos"),
    path('agregarBeneficio/<int:pk>',views.AgregarBeneficio, name="agregarBeneficio"),
    path('remove_element',views.removeElement,name="remove_element"),
]
