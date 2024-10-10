from django.contrib import admin
from .models import  Corto, Pase, UsuarioAleatorio, Votacion


admin.site.register(Corto)
admin.site.register(Pase)
admin.site.register(UsuarioAleatorio)


class VotacionAdmin(admin.ModelAdmin):
    # Muestra las columnas 'corto', 'usuario' y 'votacion' en la lista del admin
    list_display = ('corto', 'usuario', 'votacion')
admin.site.register(Votacion, VotacionAdmin)