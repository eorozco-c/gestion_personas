from django.urls import  path
from . import views

app_name = "empresas"

urlpatterns = [
    path('', views.CrearEmpresa.as_view(), name="index")
]
