from django import forms
from .models import Beneficio, ElementoBeneficio, TipoBeneficio
from django.core.exceptions import ValidationError
import datetime,math

class FormularioNuevoBeneficio(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user') 
        super(FormularioNuevoBeneficio,self ).__init__(*args,**kwargs) # populates the post
        self.fields['tipo_beneficio'].queryset = TipoBeneficio.objects.filter(empresa=self.user.empresa)

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

