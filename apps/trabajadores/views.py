from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Trabajador
from .formularios import FormularioNuevoTrabajador


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

class DetalleTrabajador(DetailView):
    template_name = "trabajadores/detalles_trabajadores.html"
    model = Trabajador

    def get_context_data(self, **kwargs):
        context = super(DetalleTrabajador, self).get_context_data(**kwargs)
        context['appname'] = "trabajadores"
        return context

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
        trabajador.delete()
    return redirect("trabajadores:index")