from django.utils.decorators import method_decorator
from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .formularios import FormularioRegistro, FormularioEditarRegistro,FormularioActualizarPass
from .models import Usuario
from apps.empresas.models import Empresa
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.

def index(request):
    if request.method == "GET":
        if Empresa.objects.count() == 0:
            return redirect("empresas:index")
        if Usuario.objects.count() == 0:
            return redirect("usuarios:register")
        if request.user.is_authenticated:
            return redirect("master:menu")
    return redirect("login")

@method_decorator(login_required, name='dispatch')
class Register(CreateView):
    template_name = "formularios/generico.html"
    form_class = FormularioRegistro
    success_url = reverse_lazy("master:index")

    def form_valid(self,form):
        usuario = form.save(commit = False)
        usuario.username = usuario.email
        usuario.set_password(usuario.password)
        usuario.save()
        login(self.request, usuario)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)
        context['title'] = "Registro" 
        context['legend'] = "Registro de usuario"
        return context

    def get(self, request):
        if self.request.user.is_superuser or Usuario.objects.count() == 0:
            return super().get(request)
        return redirect("master:index")

class Profile(UpdateView):
    template_name = "registration/perfil.html"
    model = Usuario
    form_class = FormularioEditarRegistro

    def post(self, request, *args, **kwargs):
        if "changePassword" in request.POST:
            change_pass = FormularioActualizarPass(request.POST,instance=self.request.user)
            formRegistro = FormularioEditarRegistro(instance=self.request.user)
            if change_pass.is_valid():
                usuario = change_pass.save(commit = False)
                usuario.set_password(usuario.password)
                usuario.save()
                login(request, usuario)
                messages.success(request,'Actualizado correctamente.')
                return redirect("usuarios:profile", pk=self.request.user.id)
            else:
                context = {
                    "form" : formRegistro,
                    "change_pass" : change_pass,
                }
                return render(request,"registration/perfil.html",context)
        elif "editProfile" in request.POST:
            change_pass = FormularioActualizarPass()
            formRegistro = FormularioEditarRegistro(request.POST,instance=self.request.user)
            if formRegistro.is_valid():
                usuario = formRegistro.save()
                messages.success(request,'Actualizado correctamente.')
                return redirect("usuarios:profile", pk=self.request.user.id)
            else:
                context = {
                    "formulario_reg" : formRegistro,
                    "change_pass" : change_pass,
                }
                return render(request,"registration/perfil.html",context)

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context["change_pass"] = FormularioActualizarPass(instance=self.request.user)
        return context

    def get(self, request, pk):
        usuario = self.get_object()
        if self.request.user.empresa != usuario.empresa:
            return redirect("master:index")
        return super().get(request)