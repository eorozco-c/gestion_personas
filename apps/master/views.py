from ..validaciones import obtenerUsuario
from django.shortcuts import render,HttpResponse,redirect
from ..usuarios.models import Perfil
from .formularios import FormularioForgotPassowrd

# Create your views here.
def index(request):
    if Perfil.objects.count() == 0:
        Perfil.objects.create(nombre="superadmin")
        Perfil.objects.create(nombre="admin")
    return redirect("usuarios:index")

def menu(request):
    if "id" in request.session:
        usuario = obtenerUsuario(id = request.session["id"])
        context = {
            "usuario" : usuario,
        }
        return render(request, "menu.html", context)
    return redirect("master:index")

def forgotPassword(request):
    if request.method == "GET":
        form = FormularioForgotPassowrd()
        if "id" in request.session:
             return redirect("master:index")
        context = {
            "formulario" : form,
            "title" : "Forgot Password",
            "legend" : "Olvidor su contraseña?",
        }
        return render(request,"generico.html",context)
    form = FormularioForgotPassowrd(request.POST)
    if form.is_valid():
        print("ENVIANDO CORREO")
        return redirect("master:index")
    else:
        context = {
            "formulario" : form,
            "title" : "Forgot Password",
            "legend" : "Olvido su contraseña?",
        }
        return render(request,"generico.html",context)
