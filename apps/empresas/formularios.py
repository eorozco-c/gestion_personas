from django.forms.models import model_to_dict
from django import forms
from .models import Empresa
from ..validaciones import obtenerUsuario, validarLongitud
class FormularioEmpresa(forms.ModelForm):

    class Meta:
        model = Empresa
        #fields = "__all__"
        fields = ["nombre"]

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        validarLongitud(nombre,"nombre",2,15)
        return nombre