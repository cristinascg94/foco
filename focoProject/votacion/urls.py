from django.urls import path

from votacion.views import votacion, pase, votacion_cortos, authUser,check_user, votar, generar_word

urlpatterns = [
    path('', pase, name='index'),
    path('votacion/<str:nombre_pase>/<str:usuario>/', votacion, name="votacion"),
    path('votacion_corto/<str:nombre_corto>/', votacion_cortos, name="votacion_cortos"),
    path('usuario/<str:nombre_pase>/', authUser, name="usuario"),
    path('check_user/<str:nombre_pase>/', check_user, name='check_user'),
    path('votar/', votar, name='votar'),
    path('generar_word/<str:nombre_pase>/', generar_word, name='generar_word'),
    #path('auth/<str:nombre_pase>/', authUser, name='auth_user'),
    # path('votacion/<str:nombre_pase>/<str:codigo_usuario>/', votacion, name="votacion"),
    # path('usuario/<str:nombre_pase>/', authUser_validation, name="authUser_validation")
]