from django.urls import path

from votacion.views import votacion, index, pase, votacion_cortos

urlpatterns = [
    path('', index, name='index'),
    path('votacion/<str:nombre_pase>/', votacion, name="votacion"),
    path('pase', pase, name="pase"),
    path('votacion_corto/<str:nombre_corto>/', votacion_cortos, name="votacion_cortos")
]