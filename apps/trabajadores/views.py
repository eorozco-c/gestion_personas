from apps.beneficios.models import Beneficio, ElementoBeneficio
from django.contrib import messages
from django.core.files.storage import  FileSystemStorage
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from .models import Sector, Trabajador, TrabajadorBeneficio
from .resources import TrabajadorExportResource
from .formularios import FormularioNuevoTrabajador
import csv, io, datetime, os
from apps.validaciones import validarLetrasReturn, validarRut
from apps.documentos.models import DocumentoTrabajador, TipoDocumento

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListTrabajadores(ListView):
    model = Trabajador
    template_name = "trabajadores/trabajadores.html"

    def get_queryset(self):
        queryset = Trabajador.objects.filter(empresa=self.request.user.empresa)
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateTrabajador(CreateView):
    template_name = "formularios/generico.html"
    form_class = FormularioNuevoTrabajador
    success_url = reverse_lazy("trabajadores:index")

    def form_valid(self,form):
        trabajador = form.save(commit = False)
        trabajador.empresa = self.request.user.empresa
        trabajador.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateTrabajador, self).get_context_data(**kwargs)
        context['title'] = "Nuevo Trabajador" 
        context['legend'] = "Nuevo Trabajador"
        context['appname'] = "trabajadores"
        return context
    
    def get_form_kwargs(self):
        kwargs = super(CreateTrabajador, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

@method_decorator(login_required, name='dispatch')
class DetalleTrabajador(DetailView):
    template_name = "trabajadores/detalles_trabajadores.html"
    model = Trabajador

    def get_context_data(self, **kwargs):
        context = super(DetalleTrabajador, self).get_context_data(**kwargs)
        tipo_documentos = TipoDocumento.objects.filter(empresa=self.request.user.empresa)
        documentos = DocumentoTrabajador.objects.filter(trabajador=self.object)
        beneficios = Beneficio.objects.filter(empresa=self.request.user.empresa)
        trabajador_beneficios = TrabajadorBeneficio.objects.filter(trabajador=self.object)
        context['documentos'] = documentos
        context["tipo_documentos"] = tipo_documentos
        context["beneficios"] = beneficios
        context["trabajador_beneficios"] = trabajador_beneficios
        context['appname'] = "trabajadores"
        return context
    
    def get(self, request, pk):
        trabajador = self.get_object()
        if self.request.user.empresa != trabajador.empresa:
            return redirect("master:index")
        return super().get(request)

@method_decorator(login_required, name='dispatch')
class EditTrabajador(UpdateView):
    template_name = "formularios/generico.html"
    form_class = FormularioNuevoTrabajador
    model = Trabajador
    success_url = reverse_lazy("trabajadores:index")

    def get_context_data(self, **kwargs):
        context = super(EditTrabajador, self).get_context_data(**kwargs)
        context['title'] = "Editar Trabajador" 
        context['legend'] = "Editar Trabajador"
        context['appname'] = "trabajadores"
        return context
    
    def get_form_kwargs(self):
        kwargs = super(EditTrabajador, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def get(self, request, pk):
        trabajador = self.get_object()
        if self.request.user.empresa != trabajador.empresa:
            return redirect("master:index")
        return super().get(request)

@login_required(login_url="/")
def predestroy(request, pk):
    if request.method == "GET":
        try:
            trabajador = Trabajador.objects.get(id=pk)
        except:
            return redirect("trabajadores:index")
        context={
            'id' : trabajador.id,
            'nombre': trabajador.nombre,
            'apellido' : trabajador.apellido,
            'email' : trabajador.email,
            'rut' : trabajador.rut,
            'sector' : trabajador.sector.nombre,
        }
        return JsonResponse(context)
    return redirect("trabajadores:index")

@login_required(login_url="/")
def destroy(request,pk):
    if request.method == "GET":
        try:
            trabajador = Trabajador.objects.get(id=pk)
        except:
            return redirect("trabajadores:index")
        if request.user.empresa != trabajador.empresa:
            return redirect("master:index")
        trabajador.delete()
    return redirect("trabajadores:index")

@login_required(login_url="/")
def TrabajadorExport(request):
    if request.method == "GET":
        trabajador_resource = TrabajadorExportResource()
        query = Trabajador.objects.filter(empresa=request.user.empresa)
        dataset =  trabajador_resource.export(query)
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="trabajadores.csv"'
        return response
    return redirect("trabajadores:index")

@login_required(login_url="/")
def TrabajadorImport(request):
    if request.method == 'POST':
        csv_file = request.FILES["myfile"]
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            if len(column) < 6:
                messages.success(request,f'registro {column} - Faltan campos.')
                return redirect("trabajadores:index")
            if column[5] == "F":
                genero = 1
            elif column[5] == "M":
                genero = 2
            else:
                genero = 3
            try:
                sector = Sector.objects.get(nombre__iexact=column[6])
            except:
                messages.success(request,f'registro {column} - Sector invalido.', extra_tags='danger')
                return redirect("trabajadores:index")
            try:
                fecha_nacimiento = datetime.datetime.strptime(column[4], "%d-%m-%Y")
            except:
                fecha_nacimiento = datetime.datetime.strptime(column[4], "%Y-%m-%d")
            if not validarLetrasReturn(column[0]):
                messages.success(request,f'registro {column} - nombre invalido.',extra_tags='danger')
                return redirect("trabajadores:index")
            if not validarLetrasReturn(column[1]):
                messages.success(request,f'registro {column} - apellido invalido.',extra_tags='danger')
                return redirect("trabajadores:index")
            if not validarRut(column[3]):
                messages.success(request,f'registro {column} - Rut invalido.',extra_tags='danger')
                return redirect("trabajadores:index")
            updated_values = {'nombre': column[0], 'apellido' : column[1], 'email':column[2],'fecha_nacimiento':fecha_nacimiento,'genero':genero,'sector':sector,'empresa':request.user.empresa,}
            created = Trabajador.objects.update_or_create(
                rut=column[3],
                defaults=updated_values
            )
    messages.success(request,f'registros creados correctamente.',extra_tags='success')
    return redirect("trabajadores:index")

@login_required(login_url="/")
def CargaDocumento(request, pk):
    if request.method == "POST":
        if not request.FILES:
            messages.success(request,f'Favor carge un documento',extra_tags='danger')
            return redirect("trabajadores:detail_worker", pk=pk)
        archivo = request.FILES["archivo"]
        format = False
        formatos = [".PDF",".pdf"]
        for formato in formatos:
            if formato in archivo.name:
                format = True
                break
        if format:
            tipo_documentos = request.POST["tipo_documentos"]
            fileStorage =  FileSystemStorage(f"media/trabajadores/{pk}")
            fileStorage.save(archivo.name, archivo)
            DocumentoTrabajador.objects.create(nombre=archivo,documento=f"media/trabajadores/{pk}/{archivo}",tipo_documento_id=tipo_documentos,trabajador_id=pk)
            messages.success(request,f'Cargado correctamente',extra_tags='success')
            return redirect("trabajadores:detail_worker", pk=pk)
        messages.success(request,f'Favor cargue un documento con extension .pdf',extra_tags='danger')
    return redirect("trabajadores:detail_worker", pk=pk)

@login_required(login_url="/")
def DescargaDocumento(request, pk):
    if request.method == "POST":
        ruta = request.POST["documentos"]
        if os.path.exists(ruta):
            with open(ruta,'rb') as fh:
                respuesta = HttpResponse(fh.read(), content_type="application/force_download")
                respuesta["Content-Disposition"] = f"inline; filename={os.path.basename(ruta)}"
                return respuesta
    return redirect("trabajadores:detail_worker", pk=pk)

@login_required(login_url="/")
def ElementosBeneficio(request, pk):
    if request.method == "GET":
        try:
            elementos = ElementoBeneficio.objects.filter(beneficio_id=pk,estado=False)
            data = list(elementos.values())
            context = {
                "data" : data,
            }
            return JsonResponse(context)
        except:
            return  JsonResponse({"response":"Error"})

@login_required(login_url="/")
def AgregarBeneficio(request, pk):
    if request.method == "POST":
        try:
            trabajador = Trabajador.objects.get(id=pk)
            beneficio = Beneficio.objects.get(id=request.POST["beneficios"])
            elemento = ElementoBeneficio.objects.get(id=request.POST["elementosBeneficio"])
            elemento.estado = True
            elemento.save()
            beneficioTrabajador = TrabajadorBeneficio.objects.create(trabajador=trabajador,beneficio=beneficio,elemento=elemento)
            return redirect("trabajadores:detail_worker", pk=pk)
        except:
            messages.success(request,f'Error al asignar elemento',extra_tags='danger')
            return redirect("trabajadores:detail_worker", pk=pk)

@login_required(login_url="/")
@csrf_exempt
def removeElement(request):
    try:
        elementos = request.POST.getlist("elementos[]")
        for elemento in elementos:
            e = TrabajadorBeneficio.objects.get(id=elemento)
            e.elemento.estado = False
            e.elemento.save()
            e.delete()
    except:
        return redirect("beneficios:index")
    return JsonResponse({"resultado":"eliminados correctamente"})