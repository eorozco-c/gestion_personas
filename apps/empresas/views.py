from django.shortcuts import render,redirect
from .formularios import FormularioEmpresa
from apps.validaciones import obtenerUsuario
from .models import Empresa
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# Create your views here.

class CrearEmpresa(CreateView):
    template_name = "generico.html"
    form_class = FormularioEmpresa
    success_url = reverse_lazy("master:index")

    def get_context_data(self, **kwargs):
        context = super(CrearEmpresa, self).get_context_data(**kwargs)
        context['title'] = "Nueva Empresa"
        context['legend'] = "Registro empresa"
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser or Empresa.objects.count() == 0:
            return super().get(*args, **kwargs)
        return redirect("master:index")