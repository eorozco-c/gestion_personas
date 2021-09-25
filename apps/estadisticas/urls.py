from django.urls import  path
from . import views

app_name = "estadisticas"

urlpatterns = [
    path('trabajadores-sector', views.trabajadoresSector, name="index"),
    path('populate-trabajadores-sector', views.populateTrabajadoresSector, name="populateTrabajadoresSector"),
]
