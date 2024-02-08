"""
URL configuration for JuegoPiedraPapelTijera project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    # Ruta de la página de inicio
    path('', views.home, name='home'),
    # Ruta para el coliseo donde se registran los jugadores y se inician las peleas
    path('coliseum/', views.coliseum, name='coliseum'),
    # Ruta para la página de combate entre dos jugadores
    path('combat_area/<int:player_1_id>/<int:player_2_id>/<int:fight_id>/', views.combatArea, name='combat_area'),
    # Ruta para la página de combate avanzado entre dos jugadores
    path('combat_area_up/<int:player_1_id>/<int:player_2_id>/<int:fight_id>/', views.combatAreaUp, name='combat_area_up'),
    # Ruta para la página de victoria
    path('victory/<int:fight_id>/', views.victory, name='victory'),
    # Ruta para volver a intentar una pelea
    path('try_again/<int:result>/', views.tryAgain, name='try_again')
]