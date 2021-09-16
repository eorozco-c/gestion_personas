from apps.beneficios.models import TipoBeneficio
from apps.trabajadores.models import Sector
from apps.documentos.models import TipoDocumento
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .formularios import FormularioNuevoSector, FormularioTipoBeneficio, FormularioTipoDocumento
from django.contrib import messages
# Create your views here.
def index(request):
    return redirect("master:index")

@method_decorator(login_required, name='dispatch')
class NuevoSector(ListView):
    model = Sector
    template_name = "configuraciones/sectores.html"

    def get_queryset(self):
        queryset = Sector.objects.filter(empresa=self.request.user.empresa)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(NuevoSector, self).get_context_data(**kwargs)
        context['form'] = FormularioNuevoSector()
        return context
    
    def post(self, request, *args, **kwargs):
        form = FormularioNuevoSector(request.POST)
        if form.is_valid():
            sector = form.save(commit = False)
            sector.empresa = self.request.user.empresa
            sector.save()
            messages.success(request,'Agregado correctamente.', extra_tags='success')
        return redirect("configuraciones:sectores")

@method_decorator(login_required, name='dispatch')
class EditSector(UpdateView):
    template_name = "formularios/generico.html"
    form_class = FormularioNuevoSector
    model = Sector
    success_url = reverse_lazy("configuraciones:sectores")

    def get_context_data(self, **kwargs):
        context = super(EditSector, self).get_context_data(**kwargs)
        context['title'] = "Editar Sector" 
        context['legend'] = "Editar Sector"
        context['appname'] = "configuraciones/sectores"
        return context

    def get(self, request, pk):
        sector = self.get_object()
        if self.request.user.empresa != sector.empresa:
            return redirect("master:index")
        return super().get(request)

@login_required(login_url="/")
def sectores_predestroy(request, pk):
    if request.method == "GET":
        try:
            sector = Sector.objects.get(id=pk)
        except:
            return redirect("configuraciones:sectores")
        context={
            'id' : sector.id,
            'nombre': sector.nombre,
            'direccion' : sector.direccion,
        }
        return JsonResponse(context)
    return redirect("configuraciones:sectores")

@login_required(login_url="/")
def sectores_destroy(request,pk):
    if request.method == "GET":
        try:
            sector = Sector.objects.get(id=pk)
        except:
            return redirect("configuraciones:sectores") 
        try:
            if request.user.empresa != sector.empresa:
                return redirect("master:index")
            sector.delete()
        except:
            messages.success(request,'Existen Trabajadores asociados al Sector que desea eliminar.', extra_tags='danger')
    return redirect("configuraciones:sectores")  
        
@method_decorator(login_required, name='dispatch')
class NuevoTipoDocumento(ListView):
    model = TipoDocumento
    template_name = "configuraciones/tipo_documentos.html"

    def get_queryset(self):
        queryset = TipoDocumento.objects.filter(empresa=self.request.user.empresa)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(NuevoTipoDocumento, self).get_context_data(**kwargs)
        context['form'] = FormularioTipoDocumento()
        return context
    
    def post(self, request, *args, **kwargs):
        form = FormularioTipoDocumento(request.POST)
        if form.is_valid():
            documento = form.save(commit = False)
            documento.empresa = self.request.user.empresa
            documento.save()
            messages.success(request,'Agregado correctamente.', extra_tags='success')
        return redirect("configuraciones:documentos")

@method_decorator(login_required, name='dispatch')
class EditTipoDocumento(UpdateView):
    template_name = "formularios/generico.html"
    form_class = FormularioTipoDocumento
    model = TipoDocumento
    success_url = reverse_lazy("configuraciones:documentos")

    def get_context_data(self, **kwargs):
        context = super(EditTipoDocumento, self).get_context_data(**kwargs)
        context['title'] = "Editar Tipo de documento" 
        context['legend'] = "Editar Tipo de documento"
        context['appname'] = "configuraciones/documentos"
        return context

    def get(self, request, pk):
        tipo_documento = self.get_object()
        if self.request.user.empresa != tipo_documento.empresa:
            return redirect("master:index")
        return super().get(request)

@login_required(login_url="/")
def documentos_predestroy(request, pk):
    if request.method == "GET":
        try:
            tipo_documento = TipoDocumento.objects.get(id=pk)
        except:
            return redirect("configuraciones:documentos")
        context={
            'id' : tipo_documento.id,
            'nombre': tipo_documento.nombre,
        }
        return JsonResponse(context)
    return redirect("configuraciones:documentos")

@login_required(login_url="/")
def documentos_destroy(request,pk):
    if request.method == "GET":
        try:
            tipo_documento = TipoDocumento.objects.get(id=pk)
        except:
            return redirect("configuraciones:documentos") 
        try: 
            if request.user.empresa != tipo_documento.empresa:
                return redirect("master:index")
            tipo_documento.delete()
        except:
            messages.success(request,'Existen Trabajadores o Beneficios asociados al Tipo de documento que desea eliminar.', extra_tags='danger')
    return redirect("configuraciones:documentos")  


@method_decorator(login_required, name='dispatch')
class NuevoTipoBeneficio(ListView):
    model = TipoBeneficio
    template_name = "configuraciones/tipo_beneficio.html"

    def get_queryset(self):
        queryset = TipoBeneficio.objects.filter(empresa=self.request.user.empresa)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(NuevoTipoBeneficio, self).get_context_data(**kwargs)
        context['form'] = FormularioTipoBeneficio()
        return context
    
    def post(self, request, *args, **kwargs):
        form = FormularioTipoBeneficio(request.POST)
        if form.is_valid():
            beneficio = form.save(commit = False)
            beneficio.empresa = self.request.user.empresa
            beneficio.save()
            messages.success(request,'Agregado correctamente.', extra_tags='success')
        return redirect("configuraciones:beneficios")

@method_decorator(login_required, name='dispatch')
class EditTipoBeneficio(UpdateView):
    template_name = "formularios/generico.html"
    form_class = FormularioTipoBeneficio
    model = TipoBeneficio
    success_url = reverse_lazy("configuraciones:beneficios")

    def get_context_data(self, **kwargs):
        context = super(EditTipoBeneficio, self).get_context_data(**kwargs)
        context['title'] = "Editar Tipo de beneficios" 
        context['legend'] = "Editar Tipo de beneficios"
        context['appname'] = "configuraciones/beneficios"
        return context

    def get(self, request, pk):
        tipo_beneficio = self.get_object()
        if self.request.user.empresa != tipo_beneficio.empresa:
            return redirect("master:index")
        return super().get(request)

@login_required(login_url="/")
def beneficios_predestroy(request, pk):
    if request.method == "GET":
        try:
            tipo_beneficio = TipoBeneficio.objects.get(id=pk)
        except:
            return redirect("configuraciones:beneficios")
        context={
            'id' : tipo_beneficio.id,
            'nombre': tipo_beneficio.nombre,
        }
        return JsonResponse(context)
    return redirect("configuraciones:beneficios")

@login_required(login_url="/")
def beneficios_destroy(request,pk):
    if request.method == "GET":
        try:
            tipo_beneficio = TipoBeneficio.objects.get(id=pk)
        except:
            return redirect("configuraciones:beneficios") 
        try:
            if request.user.empresa != tipo_beneficio.empresa:
                return redirect("master:index")
            tipo_beneficio.delete()
        except:
            messages.success(request,'Existen Trabajadores asociados al Beneficio que desea eliminar.', extra_tags='danger')
    return redirect("configuraciones:beneficios")