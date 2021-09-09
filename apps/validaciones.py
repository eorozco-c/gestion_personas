from django.core.exceptions import ValidationError
from .usuarios.models import Usuario
from itertools import cycle
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETTER_REGEX = re.compile(r'^[a-zA-Z]+$')
RUT_REGEX = re.compile(r'^[0-9]+\-[kK0-9]+$')

def validarLongitud(cadena,campo,minlength = 3, maxlength = 10):
    if len(cadena) < minlength or len(cadena) > maxlength:
        raise ValidationError(f"{campo} debe tener entre {minlength} y {maxlength} caracteres")

def validarEmail(email):
    if not EMAIL_REGEX.match(email):     
        raise ValidationError("Email invalido")

def validarLetras(cadena,campo):
    if not LETTER_REGEX.match(cadena):
        raise ValidationError(f"{campo} debe contener solo letras y sin espacio")

def validarRut(rut):
    if not RUT_REGEX.match(rut):
        return False
    rut = rut.upper()
    rut = rut.replace("-","")
    rut = rut.replace(".","")
    aux = rut[:-1]
    dv = rut[-1:]
    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2,8))
    s = sum(d * f for d, f in zip(revertido,factors))
    res = (-s)%11
    if str(res) == dv:
        return True
    elif dv=="K" and res==10:
        return True
    else:
        return False

def obtenerUsuario(id = None, email = None):
    try:
        if id:
            usuarioExiste = Usuario.objects.get(id = id)
        elif email:
            usuarioExiste = Usuario.objects.get(email__iexact = email)
    except:
        usuarioExiste = None
    return usuarioExiste
