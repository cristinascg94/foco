from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Pase, Corto, Votacion, UsuarioAleatorio
from django.http import JsonResponse
from docx import Document
import io
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import csv
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
import random


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def pase(request):
    pases = Pase.objects.all().order_by('orden')
    return render(request, 'pase.html', {'pases': pases})


# def votacion(request, nombre_pase, usuario):
#     print("Entro")

        
#     print(usuario)
        
#         # Asegúrate de que el código de usuario es válido
#     if usuario:
#         # Obtener el objeto Pase
#         pase = Pase.objects.get(pase=nombre_pase)
        
#         # Filtrar los cortos por el pase seleccionado
#         cortos_filtrados = Corto.objects.filter(pase=pase)
        
#         # Renderizar la plantilla con los cortos filtrados
#         return render(request, 'votacion.html', {'cortos': cortos_filtrados,
#                                                  'usuario':usuario})
    
#     # Si no se recibe un POST válido, podrías redirigir o mostrar un mensaje de error
#     return render(request, 'votacion.html', {'error_message': "No se recibió un código de usuario válido."})




def votacion(request, nombre_pase, usuario):


    # Asegúrate de que el código de usuario es válido
    if usuario:
        # Obtener el objeto Pase
        pase = Pase.objects.get(pase=nombre_pase)

        # Filtrar los cortos por el pase seleccionado
        cortos_filtrados = Corto.objects.filter(pase=pase).order_by('orden')

        # Obtener las votaciones del usuario para saber si ha editado
        votaciones_usuario = Votacion.objects.filter(usuario__nombre_usuario=usuario)

        # Crear un diccionario para fácil acceso a la edición
        votaciones_dict = {votacion.corto.id: votacion for votacion in votaciones_usuario}

        # Crear una lista de cortos con información de edición
        cortos = []
        for corto in cortos_filtrados:
            editado = corto.id in votaciones_dict  # Verifica si ha sido editado
            cortos.append({
                'id': corto.id,
                'corto': corto.corto,
                'editado': votaciones_dict.get(corto.id).edicion if editado else 0
            })

        print(cortos)

        # Renderizar la plantilla con los cortos filtrados y su información de edición
        return render(request, 'votacion.html', {'cortos': cortos, 'usuario': usuario})

    # Si no se recibe un POST válido, podrías redirigir o mostrar un mensaje de error
    return render(request, 'votacion.html', {'error_message': "No se recibió un código de usuario válido."})



def authUser(request, nombre_pase):
    error_message = None  # Inicializa la variable de error

    return render(request, 'authUser.html', {
        'nombre_pase': nombre_pase,
        'error_message': error_message,
    })


def check_user(request, nombre_pase):

    if request.method == 'POST':
        codigo_usuario = request.POST.get('codigo_usuario')
        pase = Pase.objects.get(pase=nombre_pase)
        if UsuarioAleatorio.objects.filter(nombre_usuario=codigo_usuario, pase=pase).exists():
            return JsonResponse({'exists': True}, status=200)
        else:
            return JsonResponse({'exists': False}, status=200)
    return render(request, 'check_user.html')



def votar(request):
    if request.method == 'POST':
        # Obtener datos del POST
        puntuacion = request.POST.get('puntuacion')
        corto_id = request.POST.get('corto_id')



        usuario = request.POST.get('usuario_id')

        if not usuario or not corto_id:
            return JsonResponse({'error': 'Datos incompletos'}, status=400)
        
        usuario = UsuarioAleatorio.objects.get(nombre_usuario=usuario)

        # Filtrar el objeto por usuario_id y corto_id
        votacion = get_object_or_404(Votacion, usuario_id=usuario, corto_id=corto_id)
        if votacion.edicion<1:
            votacion.edicion = 1
            votacion.votacion = puntuacion
            votacion.save()
            return JsonResponse({'exists': True}, status=200)
        else:
            return JsonResponse({'exists': False}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
def get_data_results():
    results= (Votacion.objects
            .values('corto_id')
            .annotate(total_votos=Sum('votacion'))
                .order_by('-total_votos')[:5])
    
 
    
    cortos_con_nombres = []
    for result in results:
        corto_obj = Corto.objects.get(id=result['corto_id'])
        cortos_con_nombres.append({
            'nombre': corto_obj.corto,  # Asegúrate de que el modelo Corto tiene un campo 'nombre'
            'total_votos': result['total_votos']
        })

    print(cortos_con_nombres)
    return cortos_con_nombres


@login_required
def graphicsResults(request):
    corto = get_data_results()
    return render(request, 'graphicsResults.html', {'cortos': corto})
    




def descargar_csv(request, nombre_pase=None):
    # Crear la respuesta HTTP con el tipo de contenido adecuado
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="calificaciones.csv"'

    # Crear un escritor CSV
    writer = csv.writer(response)

    # Escribir el encabezado del CSV
    writer.writerow(['corto_id', 'nombre_usuario', 'puntuacion'])

    # Consultar los datos del modelo Votacion, filtrando por nombre del pase si se proporciona
    if nombre_pase:
        # Filtrar las votaciones por el nombre del pase
        calificaciones = Votacion.objects.filter(corto__pase__pase=nombre_pase).select_related('usuario').values_list('corto_id', 'usuario__nombre_usuario')
    else:
        calificaciones = Votacion.objects.all().select_related('usuario').values_list('corto_id', 'usuario__nombre_usuario')

    # Escribir los datos en el archivo CSV
    for corto_id, nombre_usuario in calificaciones:
        # Generar un número aleatorio entre 0 y 5
        votacion_random = random.randint(0, 5)
        # Escribir la fila en el CSV
        writer.writerow([corto_id, nombre_usuario, votacion_random])

    return response


def login_view(request):
    get_token(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirigir a la vista adecuada según el tipo de usuario
            try:  # Redirigir a panel de administración si es admin
                next_url = request.GET.get('next')  # Si se solicitó otra URL
                return redirect(next_url) 
                
            except:
                return redirect('/admin/')
                 # Redirigir a una vista protegida
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')