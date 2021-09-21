from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from .models import Sector, Trabajador
from .resources import TrabajadorExportResource
from .formularios import FormularioNuevoTrabajador
import csv, io, datetime
from apps.validaciones import validarLetrasReturn, validarRut


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