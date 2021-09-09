from django.urls import  path
from . import views

app_name = "beneficios"

urlpatterns = [
    path('', views.index, name="index")
]
