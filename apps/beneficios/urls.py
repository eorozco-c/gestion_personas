from django.urls import  path
from . import views

app_name = "beneficios"

urlpatterns = [
    path('', views.ListBeneficios.as_view(), name="index"),
    path('new',views.CreateBeneficio.as_view(), name="new"),
    path('view/<int:pk>',views.DetalleBeneficio.as_view(), name="detail"),
    path('edit/<int:pk>',views.EditBeneficio.as_view(), name="edit"),
    path('predestroy/<int:pk>',views.predestroy, name="predestroy"),
    path('destroy/<int:pk>',views.destroy, name="destroy"),
    path('add_element',views.addElement,name="add_element"),
    path('remove_element',views.removeElement,name="remove_element"),
    path('export',views.BeneficioExport,name="export"),
    path('cargaDoc/<int:pk>',views.CargaDocumento, name="cargaDoc"),
    path('descargaDoc/<int:pk>',views.DescargaDocumento, name="descargaDoc"),
]
