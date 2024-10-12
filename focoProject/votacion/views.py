from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Pase, Corto, Votacion, UsuarioAleatorio
from django.http import JsonResponse
from django.db.models import Sum


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
        return render(request, 'votacion.html', {'cortos': cortos_filtrados})
    
    # Si no se recibe un POST válido, podrías redirigir o mostrar un mensaje de error
    return render(request, 'votacion.html', {'error_message': "No se recibió un código de usuario válido."})

def votacion_cortos(request, nombre_corto, usuario):
    cortos_filtrados = Corto.objects.get(corto=nombre_corto)
    votacion_filtrada = Votacion.objects.filter(corto=cortos_filtrados)

    print(votacion_filtrada)

    return render(request, 'votacion.html', {'cortos': votacion_filtrada})



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



def votar(request, nombre_pase, usuario):
    if request.method == 'POST':
        # Obtener datos del POST
        puntuacion = request.POST.get('puntuacion')
        corto_id = request.POST.get('corto_id')

        print(f"Puntuación: {puntuacion}")
        print(f"Usuario: {usuario}")
        print(f"Corto: {corto_id}")
        # Validar si los datos existen
        if not usuario or not corto_id:
            return JsonResponse({'error': 'Datos incompletos'}, status=400)

        # Filtrar el objeto por usuario_id y corto_id
        votacion = get_object_or_404(Votacion, usuario_id=usuario, corto_id=corto_id)
        
        # Actualizar el valor de la puntuacion
        votacion.puntuacion = 1
        votacion.save()
        
        return JsonResponse({'message': 'Puntuación actualizada correctamente'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
def get_data_results():
    results= (Votacion.objects
            .values('corto_id')
            .annotate(total_votos=Sum('votacion'))
                .order_by('-total_votos')[:10])
    
    cortos_con_nombres = []
    for result in results:
        corto_obj = Corto.objects.get(id=result['corto_id'])
        cortos_con_nombres.append({
            'nombre': corto_obj.corto,  # Asegúrate de que el modelo Corto tiene un campo 'nombre'
            'total_votos': result['total_votos']
        })

    return cortos_con_nombres
        
    
def graphicsResults(request):
    corto = get_data_results()
    return render(request, 'graphicsResults.html', {'corto': corto})