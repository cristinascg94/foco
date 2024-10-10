from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Pase, Corto, Votacion, UsuarioAleatorio
from django.http import JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def pase(request):
    pases = Pase.objects.all()
    return render(request, 'pase.html', {'pases': pases})


def votacion(request, nombre_pase, usuario):
    print("Entro")

        
    print(usuario)
        
        # Asegúrate de que el código de usuario es válido
    if usuario:
        # Obtener el objeto Pase
        pase = Pase.objects.get(pase=nombre_pase)
        
        # Filtrar los cortos por el pase seleccionado
        cortos_filtrados = Corto.objects.filter(pase=pase)
        
        # Renderizar la plantilla con los cortos filtrados
        return render(request, 'votacion.html', {'cortos': cortos_filtrados,
                                                 'usuario':usuario})
    
    # Si no se recibe un POST válido, podrías redirigir o mostrar un mensaje de error
    return render(request, 'votacion.html', {'error_message': "No se recibió un código de usuario válido."})

def votacion_cortos(request, nombre_corto, usuario):
    cortos_filtrados = Corto.objects.get(corto=nombre_corto)
    votacion_filtrada = Votacion.objects.filter(corto=cortos_filtrados)

    print(votacion_filtrada)

    return render(request, 'votacion.html', {'cortos': votacion_filtrada
                                             })



def authUser(request, nombre_pase):
    error_message = None  # Inicializa la variable de error
    print("Paso por aqui")

    return render(request, 'authUser.html', {
        'nombre_pase': nombre_pase,
        'error_message': error_message,
    })


def check_user(request, nombre_pase):
    print("Hola")
    if request.method == 'POST':
        codigo_usuario = request.POST.get('codigo_usuario')
        pase = Pase.objects.get(pase=nombre_pase)
        if UsuarioAleatorio.objects.filter(nombre_usuario=codigo_usuario, pase=pase).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    return render(request, 'check_user.html')



def votar(request):
    if request.method == 'POST':
        # Obtener datos del POST
        puntuacion = request.POST.get('puntuacion')
        corto_id = request.POST.get('corto_id')
        usuario = request.POST.get('usuario_id')

        print(f"Puntuación: {puntuacion}")
        print(f"Usuario: {usuario}")
        print(f"Corto: {corto_id}")
        # Validar si los datos existen
        if not usuario or not corto_id:
            return JsonResponse({'error': 'Datos incompletos'}, status=400)
        
        usuario = UsuarioAleatorio.objects.get(nombre_usuario=usuario)

        # Filtrar el objeto por usuario_id y corto_id
        votacion = get_object_or_404(Votacion, usuario_id=usuario, corto_id=corto_id)

        if votacion.edicion<1:
            votacion.edicion = 1
            votacion.votacion = puntuacion
            votacion.save()
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'message': 'Usted ya ha votado'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)