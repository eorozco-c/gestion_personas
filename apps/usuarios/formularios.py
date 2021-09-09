from django.forms.models import model_to_dict
from django import forms
from django.http import request
from .models import Usuario
from django.core.exceptions import ValidationError
from ..validaciones import obtenerUsuario, validarRut, validarLongitud, validarEmail, validarLetras
import datetime,math,bcrypt

class FormularioLogin(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ["email", "password"]
        
        widgets = {
            "password" : forms.PasswordInput(),
        }

    def clean(self):
        try:
            email = self.cleaned_data["email"]
        except: 
            raise ValidationError("Usuario o contraseña invalida")
        password = self.cleaned_data["password"]
        usuario = obtenerUsuario(email = email)
        if not usuario:
            raise ValidationError("Usuario o contraseña invalida")
        if not bcrypt.checkpw(password.encode(), usuario.password.encode()):
            raise ValidationError("Usuario o contraseña invalida")

class FormularioRegistro(forms.ModelForm):
    confirmarPassword = forms.CharField(max_length=255, label="Confirmar Password")
    confirmarPassword.widget = forms.PasswordInput()

    class Meta:
        OPCIONES_GENERO = [('1','Mujer'),('2','Hombre'),('3','Otro')]
        model = Usuario
        fields = ["nombre", "apellido","rut","fecha_nacimiento","genero","perfil","email","password","confirmarPassword","empresa"]

        widgets = {
            "fecha_nacimiento" : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs= {
                    "type" : "Date"
                }
            ),
            "password" : forms.PasswordInput(),
            "genero" : forms.RadioSelect(
                choices = OPCIONES_GENERO,
                attrs= {
                    "class" : "form-check-inline"
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

    def clean(self):
        password = self.cleaned_data["password"]
        confirm = self.cleaned_data["confirmarPassword"]
        if len(password) < 8 or len(password) > 50:
            raise ValidationError({"password" : f"password debe tener entre 8 y 50 caracteres."})
        if password != confirm:
            raise ValidationError({"password" : "Las contraseñas no coinciden."})

class FormularioEditarRegistro(forms.ModelForm):

    class Meta:
        OPCIONES_GENERO = [('1','Mujer'),('2','Hombre'),('3','Otro')]
        model = Usuario
        fields = ["nombre", "apellido","rut","fecha_nacimiento","genero","perfil","email","empresa"]

        widgets = {
            "fecha_nacimiento" : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs= {
                    "type" : "Date"
                }
            ),
            "genero" : forms.RadioSelect(
                choices = OPCIONES_GENERO,
                attrs= {
                    "class" : "form-check-inline"
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


class FormularioActualizarPass(forms.ModelForm):
    actualPassword = forms.CharField(max_length=255, label="Password Actual")
    actualPassword.widget = forms.PasswordInput()
    confirmarPassword = forms.CharField(max_length=255, label="Confirmar Password")
    confirmarPassword.widget = forms.PasswordInput()

    class Meta:
        model = Usuario
        fields = ["actualPassword","password","confirmarPassword"]

        widgets = {
            "password" : forms.PasswordInput(),
        }

    def clean(self):
        user_pass = self.instance.password
        actualPassword = self.cleaned_data["actualPassword"]
        password = self.cleaned_data["password"]
        confirm = self.cleaned_data["confirmarPassword"]
        if not bcrypt.checkpw(actualPassword.encode(), user_pass.encode()):
              raise ValidationError({"actualPassword" :"contraseña invalida"})
        if len(password) < 8 or len(password) > 50:
            raise ValidationError({"password" : f"password debe tener entre 8 y 50 caracteres."})
        if password != confirm:
            raise ValidationError({"password" : "Las contraseñas no coinciden."})