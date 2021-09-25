from django.http.response import JsonResponse
from django.shortcuts import redirect
from .formularios import FormularioEmpresa
from .models import Empresa
from apps.usuarios.models import Usuario
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.files.storage import  FileSystemStorage
import os, shutil
# Create your views here.

@method_decorator(login_required, name='dispatch')
class ListEmpresas(ListView):
    model = Empresa
    template_name = "empresas/empresas.html"


@method_decorator(login_required, name='dispatch')
class CrearEmpresa(CreateView):
    template_name = "formularios/generico.html"
    form_class = FormularioEmpresa
    success_url = reverse_lazy("empresas:index")

    def get_context_data(self, **kwargs):
        context = super(CrearEmpresa, self).get_context_data(**kwargs)
        context['title'] = "Nueva Empresa"
        context['legend'] = "Registro empresa"
        context['appname'] = "empresas"
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser or Empresa.objects.count() == 0:
            return super().get(*args, **kwargs)
        return redirect("master:index")

@method_decorator(login_required, name='dispatch')
class EditEmpresa(UpdateView):
    template_name = "empresas/detalle_empresa.html"
    model = Empresa
    form_class = FormularioEmpresa
    success_url = reverse_lazy("empresas:index")

    def get_context_data(self, **kwargs):
        context = super(EditEmpresa, self).get_context_data(**kwargs)
        context['title'] = "Editar Empresa" 
        context['legend'] = "Editar Empresa"
        context['appname'] = "empresas"
        return context

@login_required(login_url="/")
def predestroy(request, pk):
    if request.method == "GET":
        try:
            empresa = Empresa.objects.get(id=pk)
        except:
            return redirect("empresas:index")
        context={
            'id' : empresa.id,
            'nombre': empresa.nombre,
        }
        return JsonResponse(context)
    return redirect("empresas:index")

@login_required(login_url="/")
def destroy(request,pk):
    if request.method == "GET":
        try:
            empresa = Empresa.objects.get(id=pk)
        except:
            return redirect("empresas:index")
        empresa.delete()
        ruta = str(f"media/empresas/{pk}")
        if os.path.exists(ruta):
            shutil.rmtree(ruta)
    return redirect("empresas:index")

@login_required(login_url="/")
def CargaLogo(request, pk):
    if request.method == "POST":
        if not request.FILES:
            messages.success(request,f'Favor carge un documento',extra_tags='danger')
            return redirect("empresas:editar", pk=pk)
        archivo = request.FILES["archivo"]
        format = False
        formatos = [".jpg",".jpeg","png"]
        for formato in formatos:
            if formato in archivo.name:
                format = True
                break
        if format:
            ruta = str(f"media/empresas/{pk}")
            if os.path.exists(ruta):
                shutil.rmtree(ruta)
            fileStorage =  FileSystemStorage(ruta)
            fileStorage.save(archivo.name, archivo)
            try:
                empresa = Empresa.objects.get(id=pk)
            except:
                return redirect("empresas:editar", pk=pk)
            empresa.logo = f"/{ruta}/{archivo}"
            empresa.save()
            messages.success(request,f'Cargado correctamente',extra_tags='success')
            return redirect("empresas:editar", pk=pk)
        messages.success(request,f'Favor cargue una imagen',extra_tags='danger')
    return redirect("empresas:editar", pk=pk)

@login_required(login_url="/")
def cambiarEmpresa(request, pk):
    if request.method == "GET":
        print(pk)
        empresa = Empresa.objects.get(id=pk)
        usuario = Usuario.objects.get(id=request.user.id)
        usuario.empresa = empresa
        usuario.save()
    return redirect("empresas:index")