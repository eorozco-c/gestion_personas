from django.urls import  path
from . import views

app_name = "estadisticas"

urlpatterns = [
    path('', views.index, name="index"),
    path('trabajadores-sector', views.trabajadoresSector, name="trabajadoresSector"),
]
