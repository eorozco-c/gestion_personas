from django.forms.models import model_to_dict
from django import forms
from ..usuarios.models import Usuario
from django.core.exceptions import ValidationError
from ..validaciones import obtenerUsuario,validarEmail

class FormularioForgotPassowrd(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ["email"]

    def clean(self):
        try:
            email = self.cleaned_data["email"]
        except: 
            raise ValidationError({"email":"Usuario no existe"})
        usuario = obtenerUsuario(email = email)
        if not usuario:
            raise ValidationError({"email":"Usuario no existe"})
