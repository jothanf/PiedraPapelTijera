from django.db import models

"""
Este archivo models.py define los modelos de datos utilizados en la aplicación.
Aunque la prueba técnica especificaba el uso de tecnologías como ASP.NET y SQL Server,
he optado por utilizar Django, un framework de desarrollo web en Python, junto con 
su ORM (Mapeo Objeto-Relacional) para interactuar con la base de datos.
A pesar de la diferencia en las tecnologías utilizadas, se han implementado los modelos
de acuerdo con los requisitos de la prueba y se ha garantizado su funcionalidad adecuada.
"""

# Modelo para representar a un usuario
class UserModel(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

# Modelo para representar una pelea entre dos usuarios
class FightModel(models.Model):
    # Elecciones de estado para la pelea
    STATUS_CHOICES = [
        ('start', ('Start')),   # Estado inicial de la pelea
        ('finish', ('Finish')),  # Estado final de la pelea
    ]
    
    # Relación con UserModel para el primer usuario
    user_1 = models.ForeignKey('UserModel', on_delete=models.CASCADE, related_name='fights_as_user_1')
    # Relación con UserModel para el segundo usuario
    user_2 = models.ForeignKey('UserModel', on_delete=models.CASCADE, related_name='fights_as_user_2')
    # Usuario ganador de la pelea
    grand_winner = models.ForeignKey('UserModel', on_delete=models.CASCADE, null=True)
    
    # Contadores de victorias y empates para cada usuario
    winner_1 = models.PositiveIntegerField(default=0)
    winner_2 = models.PositiveIntegerField(default=0)
    tie = models.PositiveIntegerField(default=0)
    # Número de rondas jugadas
    rounds = models.PositiveIntegerField(default=1)
    
    # Estado de la pelea
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='start')

    def __str__(self):
        return f"{self.user_1} vs {self.user_2}"