from django.shortcuts import render,redirect
from apps.usuarios.models import Perfil
from apps.trabajadores.models import Trabajador
from apps.beneficios.models import Beneficio
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if Perfil.objects.count() == 0:
        Perfil.objects.create(nombre="superadmin")
        Perfil.objects.create(nombre="admin")
    return redirect("usuarios:index")

@login_required(login_url='/')
def menu(request):
    context = {
        "trabajadores" : Trabajador.objects.filter(empresa=request.user.empresa).count(),
        "beneficios" : Beneficio.objects.filter(empresa=request.user.empresa).count,
    }
    return render(request, "menu.html", context)
