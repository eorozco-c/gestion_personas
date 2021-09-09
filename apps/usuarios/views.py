from ..validaciones import obtenerUsuario
from django.shortcuts import render,HttpResponse,redirect
from .formularios import FormularioRegistro, FormularioLogin, FormularioEditarRegistro,FormularioActualizarPass
from .models import Usuario
from ..empresas.models import Empresa
import bcrypt
# Create your views here.


def index(request):
    if request.method == "GET":
        if "id" in request.session:
            return redirect("master:menu")
        if Empresa.objects.count() == 0:
            return redirect("empresas:index")
        if Usuario.objects.count() == 0:
            return redirect("usuarios:register")
        return redirect("usuarios:login")

def register(request):
    if request.method == "GET":
        if "id" in request.session:
            form = FormularioRegistro()
            context = {
                "formulario" : form,
                "title" : "Registro",
                "legend" : "Registro de usuario",
                "usuario" : obtenerUsuario(id = request.session["id"])
            }
            return render(request,"generico.html",context)
        if Usuario.objects.count() == 0:
            form = FormularioRegistro()
            context = {
                "formulario" : form,
                "title" : "Registro",
                "legend" : "Registro de administración",
            }
            return render(request,"generico.html",context)
        return redirect("master:index")
    else:
        formRegistro = FormularioRegistro(request.POST)
        if formRegistro.is_valid():
            usuario = formRegistro.save(commit = False)
            password_hs = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            usuario.password = password_hs.decode()
            usuario.save()
            request.session["id"] = usuario.id
            return redirect("master:index")
        else:
            context = {
                "formulario" : formRegistro,
                "title" : "Registro",
                "legend" : "Registro de administración",
            }
            return render(request,"generico.html",context)


def login(request):
    if request.method == "GET":
        if "id" in request.session:
            return redirect("master:menu")
        form = FormularioLogin()
        context = {
            "formulario" : form,
            "title" : "Login",
            "legend" : "Gestion de Personas",
        }
        return render(request,"generico.html",context)
    else:
        formLogin = FormularioLogin(request.POST)
        if formLogin.is_valid():
            usuario = obtenerUsuario(email = request.POST["email"])
            request.session["id"] = usuario.id
            return redirect("master:menu")
        else:
            context = {
                "formulario" : formLogin,
                "title" : "Login",
                "legend" : "Gestion de Personas",
            }
            return render(request,"generico.html",context)


def logout(request):
    if request.method == "GET":
        if "id" in request.session:
            del request.session['id']
        return redirect("master:index")

def profile(request):
    if request.method == "GET":
        if "id" in request.session:
            usuario = obtenerUsuario(id = request.session["id"])
            form = FormularioEditarRegistro(instance=usuario)
            change_pass = FormularioActualizarPass(instance=usuario)
            context = {
                "formulario_reg" : form,
                "change_pass" : change_pass,
                "usuario" : usuario
            }
            return render(request,"perfil.html",context)
        return redirect("master:index")
    else:
        if "id" in request.session:
            usuario = obtenerUsuario(id = request.session["id"])

            print(request.POST)
            if "changePassword" in request.POST:
                change_pass = FormularioActualizarPass(request.POST,instance=usuario)
                formRegistro = FormularioEditarRegistro(instance=usuario)
                if change_pass.is_valid():
                    usuario = change_pass.save(commit = False)
                    password_hs = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
                    usuario.password = password_hs.decode()
                    usuario.save()
                    return redirect("usuarios:profile")
                else:
                    context = {
                        "formulario_reg" : formRegistro,
                        "change_pass" : change_pass,
                        "usuario" : usuario,
                    }
                    return render(request,"perfil.html",context)
            elif "editProfile" in request.POST:
                change_pass = FormularioActualizarPass()
                formRegistro = FormularioEditarRegistro(request.POST,instance=usuario)
                if formRegistro.is_valid():
                    usuario = formRegistro.save(commit = False)
                    usuario.save()
                    return redirect("usuarios:profile")
                else:
                    context = {
                        "formulario_reg" : formRegistro,
                        "change_pass" : change_pass,
                        "usuario" : usuario,
                    }
                    return render(request,"perfil.html",context)
    return redirect("master:index")

def change_pass(request):
    if "id" in request.session:
        usuario = obtenerUsuario(id = request.session["id"])
        formRegistro = FormularioEditarRegistro(request.POST)
        change_pass = FormularioActualizarPass(request.POST)
        if change_pass.is_valid():
            usuario = formRegistro.save(commit = False)
            password_hs = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            usuario.password = password_hs.decode()
            usuario.save()
            return redirect("usuarios:profile")
        else:
            context = {
                "formulario_reg" : formRegistro,
                "change_pass" : change_pass,
                "usuario" : usuario,
            }
            return render(request,"perfil.html",context)
    return redirect("usuarios:profile")