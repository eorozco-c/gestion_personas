from django import forms
from .models import Trabajador
from django.core.exceptions import ValidationError
from ..validaciones import validarRut, validarLongitud, validarEmail, validarLetras
import datetime,math

class FormularioNuevoTrabajador(forms.ModelForm):

    class Meta:
        OPCIONES_GENERO = [('1','Mujer'),('2','Hombre'),('3','Otro')]
        model = Trabajador
        fields = ["nombre", "apellido","rut","fecha_nacimiento","genero","email","sector"]

        widgets = {
            "fecha_nacimiento" : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs= {
                    "type" : "Date"
                }
            ),
            "genero" : forms.RadioSelect(
                choices = OPCIONES_GENERO,
                attrs={
                    "class": "algo"
                }
            ),
        }


    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        validarLetras(nombre,"nombre")
        validarLongitud(nombre,"nombre",2,15)
        return nombre
    
    def clean_apellido(self):
        apellido = self.cleaned_data["apellido"]
        validarLetras(apellido,"apellido")
        validarLongitud(apellido,"apellido",2,15)
        return apellido
    
    def clean_rut(self):
        rut = self.cleaned_data["rut"]
        validarLongitud(rut,"rut",2,15)
        if validarRut(rut) == False:
            raise ValidationError("Rut Invalido")
        return rut

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data["fecha_nacimiento"]
        today = datetime.date.today()
        edad = today-fecha_nacimiento
        edad = math.floor(edad.days/365)
        if fecha_nacimiento >= today:
            raise ValidationError("La fecha de nacimiento no es valida.")
        if edad < 13:
            raise ValidationError("La edad debe ser mayor a 13 años")
        return fecha_nacimiento
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        validarEmail(email)
        return email

