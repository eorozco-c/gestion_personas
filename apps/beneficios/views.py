from apps.documentos.models import DocumentoBeneficio, DocumentoTrabajador, TipoDocumento
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from .models import Beneficio, ElementoBeneficio
from .formularios import FormularioNuevoBeneficio
from .resources import BeneficioExportResource
from django.core.files.storage import  FileSystemStorage
import os, shutil

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListBeneficios(ListView):
    model = Beneficio
    template_name = "beneficios/beneficios.html"

    def get_queryset(self):
        queryset = Beneficio.objects.filter(empresa=self.request.user.empresa)
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateBeneficio(CreateView):
    template_name = "formularios/generico.html"
    form_class = FormularioNuevoBeneficio
    success_url = reverse_lazy("beneficios:index")

    def form_valid(self,form):
        beneficio = form.save(commit = False)
        beneficio.empresa = self.request.user.empresa
        beneficio.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateBeneficio, self).get_context_data(**kwargs)
        context['title'] = "Nuevo Beneficio" 
        context['legend'] = "Nuevo Beneficio"
        context['appname'] = "beneficios"
        return context
    
    def get_form_kwargs(self):
        kwargs = super(CreateBeneficio, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class DetalleBeneficio(DetailView):
    template_name = "beneficios/detalles_beneficios.html"
    model = Beneficio

    def get_context_data(self, **kwargs):
        context = super(DetalleBeneficio, self).get_context_data(**kwargs)
        tipo_documentos = TipoDocumento.objects.filter(empresa=self.request.user.empresa)
        documentos = DocumentoBeneficio.objects.filter(beneficio=self.object)
        context['documentos'] = documentos
        context["tipo_documentos"] = tipo_documentos
        context['appname'] = "beneficios"
        return context
    
    def get(self, request, pk):
        beneficio = self.get_object()
        if self.request.user.empresa != beneficio.empresa:
            return redirect("master:index")
        return super().get(request)

@method_decorator(login_required, name='dispatch')
class EditBeneficio(UpdateView):
    template_name = "beneficios/editar_beneficios.html"
    model = Beneficio
    form_class = FormularioNuevoBeneficio
    success_url = reverse_lazy("beneficios:index")

    def get_context_data(self, **kwargs):
        context = super(EditBeneficio, self).get_context_data(**kwargs)
        context["elementos"] = ElementoBeneficio.objects.filter(beneficio=self.object)
        context['title'] = "Editar Beneficio" 
        context['legend'] = "Editar Beneficio"
        context['appname'] = "beneficios"
        return context

    def get_form_kwargs(self):
        kwargs = super(EditBeneficio, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get(self, request, pk):
        beneficio = self.get_object()
        if self.request.user.empresa != beneficio.empresa:
            return redirect("master:index")
        return super().get(request)

@login_required(login_url="/")
@csrf_exempt
def addElement(request):
    try:
        pk = request.POST["pk"]
        input_elemento = request.POST["input_elemento"]
        beneficio = Beneficio.objects.get(id=pk)
    except:
        return redirect("beneficios:index")
    nuevo_elemento = ElementoBeneficio.objects.create(beneficio=beneficio, nombre=input_elemento)
    return JsonResponse({"resultado":"200"})


@login_required(login_url="/")
@csrf_exempt
def removeElement(request):
    try:
        pk = request.POST["pk"]
        elementos = request.POST.getlist("elementos[]")
        for elemento in elementos:
            e = ElementoBeneficio.objects.get(id=elemento)
            e.delete()
    except:
        return redirect("beneficios:index")
    return JsonResponse({"resultado":"eliminados correctamente"})

@login_required(login_url="/")
def predestroy(request, pk):
    if request.method == "GET":
        try:
            beneficio = Beneficio.objects.get(id=pk)
        except:
            return redirect("beneficios:index")
        context={
            'id' : beneficio.id,
            'nombre': beneficio.nombre,
            'fecha_inicio' : beneficio.fecha_inicio,
            'fecha_fin' : beneficio.fecha_fin,
        }
        return JsonResponse(context)
    return redirect("beneficios:index")

@login_required(login_url="/")
def destroy(request,pk):
    if request.method == "GET":
        try:
            beneficio = Beneficio.objects.get(id=pk)
        except:
            return redirect("beneficios:index")
        if request.user.empresa != beneficio.empresa:
            return redirect("master:index")
        beneficio.delete()
    return redirect("beneficios:index")

@login_required(login_url="/")
def BeneficioExport(request):
    if request.method == "GET":
        beneficio_resource = BeneficioExportResource()
        query = Beneficio.objects.filter(empresa=request.user.empresa)
        dataset =  beneficio_resource.export(query)
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="beneficios.csv"'
        return response
    return redirect("beneficios:index")

@login_required(login_url="/")
def CargaDocumento(request, pk):
    if request.method == "POST":
        if not request.FILES:
            messages.success(request,f'Favor carge un documento',extra_tags='danger')
            return redirect("beneficios:detail", pk=pk)
        archivo = request.FILES["archivo"]
        format = False
        formatos = [".PDF",".pdf"]
        for formato in formatos:
            if formato in archivo.name:
                format = True
                break
        if format:
            tipo_documentos = request.POST["tipo_documentos"]
            fileStorage =  FileSystemStorage(f"media/beneficios/{pk}")
            fileStorage.save(archivo.name, archivo)
            DocumentoBeneficio.objects.create(nombre=archivo,documento=f"media/beneficios/{pk}/{archivo}",tipo_documento_id=tipo_documentos,beneficio_id=pk)
            messages.success(request,f'Cargado correctamente',extra_tags='success')
            return redirect("beneficios:detail", pk=pk)
        messages.success(request,f'Favor cargue un documento con extension .pdf',extra_tags='danger')
    return redirect("beneficios:detail", pk=pk)

@login_required(login_url="/")
def DescargaDocumento(request, pk):
    if request.method == "POST":
        ruta = request.POST["documentos"]
        if os.path.exists(ruta):
            with open(ruta,'rb') as fh:
                respuesta = HttpResponse(fh.read(), content_type="application/force_download")
                respuesta["Content-Disposition"] = f"inline; filename={os.path.basename(ruta)}"
                return respuesta
    return redirect("beneficios:detail", pk=pk)