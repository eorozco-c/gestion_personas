from django.urls import  path
from . import views

app_name = "documentos"

urlpatterns = [
    path('', views.index, name="index")
]
