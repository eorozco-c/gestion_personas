from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Beneficio, ElementoBeneficio
from .formularios import FormularioNuevoBeneficio


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

class DetalleBeneficio(DetailView):
    template_name = "beneficios/detalles_beneficios.html"
    model = Beneficio

    def get_context_data(self, **kwargs):
        context = super(DetalleBeneficio, self).get_context_data(**kwargs)
        context['appname'] = "beneficios"
        return context

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

# @login_required(login_url="/")
# def predestroy(request, pk):
#     if request.method == "GET":
#         try:
#             trabajador = Trabajador.objects.get(id=pk)
#         except:
#             return redirect("trabajadores:index")
#         context={
#             'id' : trabajador.id,
#             'nombre': trabajador.nombre,
#             'apellido' : trabajador.apellido,
#             'email' : trabajador.email,
#             'rut' : trabajador.rut,
#             'sector' : trabajador.sector.nombre,
#         }
#         return JsonResponse(context)
#     return redirect("trabajadores:index")

# @login_required(login_url="/")
# def destroy(request,pk):
#     if request.method == "GET":
#         try:
#             trabajador = Trabajador.objects.get(id=pk)
#         except:
#             return redirect("trabajadores:index")
#         trabajador.delete()
#     return redirect("trabajadores:index")

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
    # elemento.delete()
    return JsonResponse({"resultado":"eliminados correctamente"})