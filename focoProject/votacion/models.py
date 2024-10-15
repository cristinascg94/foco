from django.db import models
import random
import string
import random
import string



class UsuarioAleatorio(models.Model):
    nombre_usuario = models.CharField(max_length=10, unique=True)
    pase = models.ForeignKey('Pase', on_delete=models.CASCADE, related_name='usuarios')

    def __str__(self):
        return self.nombre_usuario

    @staticmethod
    def generar_usuario_aleatorio():
        """Genera un nombre de usuario aleatorio que es único en la base de datos"""
        while True:
            caracteres = string.ascii_letters + string.digits
            nuevo_usuario = ''.join(random.choices(caracteres, k=6)).capitalize()
            if not UsuarioAleatorio.objects.filter(nombre_usuario=nuevo_usuario).exists():
                return nuevo_usuario


class Pase(models.Model):
    pase = models.CharField(max_length=255)
    activa = models.BooleanField(default=True)
    orden = models.IntegerField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Pase, self).save(*args, **kwargs)
        
        # Generar 300 usuarios únicos si no existen ya para este pase
        if not self.usuarios.exists():
            usuarios_nuevos = [
                UsuarioAleatorio(
                    nombre_usuario=UsuarioAleatorio.generar_usuario_aleatorio(),
                    pase=self
                ) for _ in range(300)
            ]
            UsuarioAleatorio.objects.bulk_create(usuarios_nuevos)

    def __str__(self):
        return self.pase


class Corto(models.Model):
    id = models.AutoField(primary_key=True)
    corto = models.CharField(max_length=255)
    pase = models.ForeignKey('Pase', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Corto, self).save(*args, **kwargs)
        
        # Obtener los usuarios asociados con este pase
        usuarios = self.pase.usuarios.all()
        
        # Crear una lista para almacenar las nuevas instancias de Votacion
        votaciones = []
        
        # Vincular cada usuario al corto a través del modelo Votacion, solo si no existe una votación previa
        for usuario in usuarios:
            votacion, created = Votacion.objects.get_or_create(corto=self, usuario=usuario)
            
            if created:
                # Si la votación es nueva, establecer votacion y edicion en 0
                votacion.votacion = 0
                votacion.edicion = 0
                votaciones.append(votacion)  # Añadir la nueva votación a la lista para crearla en batch
            else:
                # Si ya existe, actualizar los campos votacion y edicion a 0
                votacion.votacion = 0
                votacion.edicion = 0
                votacion.save()  # Guardar la votación existente actualizada
        
        # Crear todas las nuevas instancias de Votacion de una vez
        if votaciones:
            Votacion.objects.bulk_create(votaciones)

    def __str__(self):
        return self.corto


class Votacion(models.Model):
    corto = models.ForeignKey('Corto', on_delete=models.CASCADE, related_name='votaciones')
    usuario = models.ForeignKey('UsuarioAleatorio', on_delete=models.CASCADE, related_name='votaciones')
    votacion = models.IntegerField(default=0)
    edicion = models.IntegerField(default=0)

    class Meta:
        # Garantiza que no haya más de una votación por cada combinación de corto y usuario
        constraints = [
            models.UniqueConstraint(fields=['corto', 'usuario'], name='unique_corto_usuario')
        ]


    def __str__(self):
        return f"Votación de {self.usuario.nombre_usuario} para {self.corto.corto}: {self.votacion}"


