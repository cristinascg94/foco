from django.db import models
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
            prefix = ''.join(random.choices(string.ascii_lowercase, k=2))
            suffix = ''.join(random.choices(string.digits, k=3))
            nuevo_usuario = f'{prefix}{suffix}'
            if not UsuarioAleatorio.objects.filter(nombre_usuario=nuevo_usuario).exists():
                return nuevo_usuario


class Pase(models.Model):
    pase = models.CharField(max_length=255)
    activa = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(Pase, self).save(*args, **kwargs)
        
        # Generar 300 usuarios únicos si no existen ya para este pase
        if not self.usuarios.exists():
            for _ in range(300):
                UsuarioAleatorio.objects.create(
                    nombre_usuario=UsuarioAleatorio.generar_usuario_aleatorio(),
                    pase=self
                )

    def __str__(self):
        return self.pase


class Corto(models.Model):
    corto = models.CharField(max_length=255)
    pase = models.ForeignKey('Pase', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Corto, self).save(*args, **kwargs)
        
        # Obtener los usuarios asociados con este pase
        usuarios = self.pase.usuarios.all()
        
        # Vincular cada usuario al corto a través del modelo Votacion
        for usuario in usuarios:
            Votacion.objects.create(
                corto=self,
                usuario=usuario,
                votacion=0  # Valor inicial de la votación
            )

    def __str__(self):
        return self.corto


class Votacion(models.Model):
    corto = models.ForeignKey('Corto', on_delete=models.CASCADE, related_name='votaciones')
    usuario = models.ForeignKey('UsuarioAleatorio', on_delete=models.CASCADE, related_name='votaciones')
    votacion = models.IntegerField(default=0)
    edicion = models.IntegerField(default=0)


    def __str__(self):
        return f"Votación de {self.usuario.nombre_usuario} para {self.corto.corto}: {self.votacion}"
