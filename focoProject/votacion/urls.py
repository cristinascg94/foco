from django.urls import path

from votacion.views import votacion, pase, votacion_cortos, authUser,check_user, votar, graphicsResults, descargar_csv

urlpatterns = [
    path('', pase, name='index'),
    path('votacion/<str:nombre_pase>/<str:usuario>/', votacion, name="votacion"),
    path('votacion_corto/<str:nombre_corto>/', votacion_cortos, name="votacion_cortos"),
    path('usuario/<str:nombre_pase>/', authUser, name="usuario"),
    path('check_user/<str:nombre_pase>/', check_user, name='check_user'),
    path('votar/', votar, name='votar'),
    path('descargar-calificaciones-csv/', descargar_csv, name='descargar_calificaciones_csv'),
    path('resultados/', graphicsResults, name='graphicsResults'),

]

