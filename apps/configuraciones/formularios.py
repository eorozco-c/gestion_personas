from django import forms
from apps.beneficios.models import  TipoBeneficio
from apps.trabajadores.models import Sector
from apps.documentos.models import TipoDocumento
from apps.validaciones import validarLetras, validarLongitud

class FormularioNuevoSector(forms.ModelForm):

    class Meta:
        model = Sector
        fields = ["nombre", "direccion"]

        widgets = {
            "nombre" : forms.TextInput(
                attrs= {
                    "class" : "ms-2 mb-1 d-inline"
                },
            ),     
            "direccion" : forms.TextInput(
                attrs= {
                    "class" : "ms-2 mb-3 d-inline"
                },
            ),
        }

class FormularioTipoDocumento(forms.ModelForm):

    class Meta:
        model = TipoDocumento
        fields = ["nombre"]

        widgets = {
            "nombre" : forms.TextInput(
                attrs= {
                    "class" : "ms-2 mb-1 d-inline"
                },
            ),     
        }

class FormularioTipoBeneficio(forms.ModelForm):

    class Meta:
        model = TipoBeneficio
        fields = ["nombre"]

        widgets = {
            "nombre" : forms.TextInput(
                attrs= {
                    "class" : "ms-2 mb-1 d-inline"
                },
            ),     
        }