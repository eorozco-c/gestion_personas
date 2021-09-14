from django import forms
from .models import Beneficio, ElementoBeneficio
from django.core.exceptions import ValidationError
import datetime,math

class FormularioNuevoBeneficio(forms.ModelForm):

    class Meta:
        model = Beneficio
        fields = "__all__"
        exclude = ["empresa"]

        widgets = {
            "fecha_inicio" : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs= {
                    "type" : "Date"
                }
            ),
            "fecha_fin" : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs= {
                    "type" : "Date"
                }
            ),
        }

class FormularioEditarBeneficio(forms.ModelForm):

    class Meta:
        model = ElementoBeneficio
        fields = "__all__"


    # def clean_fecha_nacimiento(self):
    #     fecha_nacimiento = self.cleaned_data["fecha_nacimiento"]
    #     today = datetime.date.today()
    #     edad = today-fecha_nacimiento
    #     edad = math.floor(edad.days/365)
    #     if fecha_nacimiento >= today:
    #         raise ValidationError("La fecha de nacimiento no es valida.")
    #     if edad < 13:
    #         raise ValidationError("La edad debe ser mayor a 13 años")
    #     return fecha_nacimiento
