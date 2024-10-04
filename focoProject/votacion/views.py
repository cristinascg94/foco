from django.shortcuts import render
from django.http import HttpResponse
from .models import Pase, Corto, Votacion


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# def home(request):
#     contexto = {
#         'mensaje': '¡Hola desde Django!'
#     }
#     return render(request, 'home.html', contexto)

# def pase(request):
#     contexto = {
#         'mensaje': '¡Hola desde Django!'
#     }
#     return render(request, 'pase.html', contexto)

# def pase1(request):
#     contexto = {
#         'mensaje': 'Pase 1'
#     }
#     return render(request, 'pase1.html', contexto)


def pase(request):
    pases = Pase.objects.all()
    return render(request, 'pase.html', {'pases': pases})


def votacion(request, nombre_pase):
    # Filtrar los cortos por el pase seleccionado
    pases_filtrados = Pase.objects.get(pase=nombre_pase)
    cortos_filtrados = Corto.objects.filter(pase=pases_filtrados)
    
    return render(request, 'votacion.html', {'cortos': cortos_filtrados})

def votacion_cortos(request, nombre_corto):
    cortos_filtrados = Corto.objects.get(corto=nombre_corto)
    votacion_filtrada = Votacion.objects.filter(corto=cortos_filtrados)