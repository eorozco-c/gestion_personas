from apps.trabajadores.models import Sector, Trabajador
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/")
def index(request):
    return render(request,"estadisticas/trabajadores-sitios.html")

@login_required(login_url="/")
def trabajadoresSector(request):
    if request.method == "GET":
        labels = []
        data = []
        try:
            queryset = Trabajador.objects.filter(empresa=request.user.empresa).values('sector__nombre').annotate(trabajador_sector=Count('id'))
            for entry  in queryset:
                labels.append(entry['sector__nombre'])
                data.append(entry['trabajador_sector'])
            context = {
                "labels" : labels,
                "data" : data,
            }
            return JsonResponse(context)
        except:
            return  JsonResponse({"response":"Error"})