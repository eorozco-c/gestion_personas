from ..validaciones import obtenerUsuario
from django.shortcuts import render,HttpResponse,redirect
from .formularios import FormularioEmpresa
from .models import Empresa
# Create your views here.
def index(request):
    usuario = obtenerUsuario(id = request.session["id"])
    if request.method == "GET":
        if Empresa.objects.count() != 0 and usuario.perfil.id != 1:
            return redirect("master:index")
        form = FormularioEmpresa()
        context = {
            "formulario" : form,
            "title" : "Nueva Empresa",
            "legend" : "Registro empresa",
            "usuario" : usuario,
        }
        return render(request,"generico.html",context)
    formEmpresa = FormularioEmpresa(request.POST)
    if formEmpresa.is_valid():
        formEmpresa.save()
    else:
        context = {
            "formulario" : formEmpresa,
            "title" : "Nueva Empresa",
            "legend" : "Registro empresa",
            "usuario" : usuario,
        }
        return render(request,"generico.html",context)
    return redirect("master:index")
