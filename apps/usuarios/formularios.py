from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
from ..validaciones import obtenerUsuario, validarRut, validarLongitud, validarEmail, validarLetras
import datetime,math

class FormularioRegistro(forms.ModelForm):
    confirmarPassword = forms.CharField(max_length=255, label="Confirmar Password")
    confirmarPassword.widget = forms.PasswordInput()

    class Meta:
        OPCIONES_GENERO = [('1','Mujer'),('2','Hombre'),('3','Otro')]
        model = Usuario
        # fields = "__all__"
        fields = ["first_name", "last_name","rut","fecha_nacimiento","genero","is_superuser", "is_staff","email","password","confirmarPassword","empresa"]

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
                ),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        validarLetras(first_name,"first_name")
        validarLongitud(first_name,"nombre",2,15)
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        validarLetras(last_name,"last_name")
        validarLongitud(last_name,"apellido",2,15)
        return last_name
    
    def clean_rut(self):
        rut = self.cleaned_data["rut"]
        validarLongitud(rut,"rut",2,15)
        if validarRut(rut) == False:
            raise ValidationError("Rut Invalido")
        try:
            Usuario.objects.get(rut=rut)
        except:
            return rut
        raise ValidationError("Rut ya existe")

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
        usuario = obtenerUsuario(email=email)
        if usuario:
            raise ValidationError("Correo ya existe")
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
        fields = ["first_name", "last_name","rut","fecha_nacimiento","genero","email"]

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
        usuario = self.instance
        if usuario:
            actualPassword = self.cleaned_data["actualPassword"]
            password = self.cleaned_data["password"]
            confirm = self.cleaned_data["confirmarPassword"]
            if not usuario.check_password(actualPassword):
                raise ValidationError({"actualPassword" :"contraseña invalida"})
            if len(password) < 8 or len(password) > 50:
                raise ValidationError({"password" : f"password debe tener entre 8 y 50 caracteres."})
            if password != confirm:
                raise ValidationError({"password" : "Las contraseñas no coinciden."})
        else:
            raise ValidationError({"password" : "Usuario no existe."})