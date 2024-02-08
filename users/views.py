from django.shortcuts import render, redirect
from django.http import Http404
from .models import UserModel, FightModel
from .utils import fightFun, fightFun2, winner_match

# Vista para la página de inicio
def home(request):
    return render(request, 'home.html')

# Vista para el registro de jugadores y creación de la pelea
def coliseum(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            name_1 = request.POST.get('name_1')
            last_name_1 = request.POST.get('last_name_1')
            name_2 = request.POST.get('name_2')
            last_name_2 = request.POST.get('last_name_2')
            # Crear instancias de UserModel para cada jugador
            player_1 = UserModel(name=name_1, last_name=last_name_1)
            player_2 = UserModel(name=name_2, last_name=last_name_2)
            # Guardar los jugadores en la base de datos
            player_1.save()
            player_2.save()
            # Crear una nueva instancia de FightModel para la pelea entre los jugadores
            new_fight = FightModel(user_1=player_1, user_2=player_2)
            new_fight.save()
            # Redirigir a la página de combate dependiendo de la opción elegida por el usuario
            up_level = request.POST.get('up_level', False)
            if up_level:
                return redirect('combat_area_up', player_1_id=player_1.id, player_2_id=player_2.id, fight_id=new_fight.id)
            return redirect('combat_area', player_1_id=player_1.id, player_2_id=player_2.id, fight_id=new_fight.id)
        except Exception as e:
            # Manejar cualquier excepción que ocurra durante el proceso de registro
            return render(request, 'error.html', {'error_message': str(e)})
    return render(request, 'coliseum.html')

# Vista para volver a intentar una pelea
def tryAgain(request, result):
    try:
        # Obtener la pelea anterior y los jugadores involucrados
        last_fight = FightModel.objects.get(id=result)
        player_1_id = last_fight.user_1_id
        player_1 = UserModel.objects.get(id=player_1_id)
        player_2_id = last_fight.user_2_id
        player_2 = UserModel.objects.get(id=player_2_id)
        # Crear una nueva instancia de FightModel para la nueva pelea
        new_fight = FightModel(user_1=player_1, user_2=player_2)
        new_fight.save()
        # Redirigir a la página de combate con la nueva pelea
        return redirect('combat_area', player_1_id=player_1.id, player_2_id=player_2.id, fight_id=new_fight.id)
    except FightModel.DoesNotExist:
        # Manejar el caso en el que la pelea anterior no exista
        raise Http404("La pelea no existe")

# Vista para la página de combate
def combatArea(request, player_1_id, player_2_id, fight_id):
    try:
        # Obtener los jugadores y la pelea actual
        player_1 = UserModel.objects.get(id=player_1_id)
        player_2 = UserModel.objects.get(id=player_2_id)
        fight = FightModel.objects.get(id=fight_id)
        
        context = {
            'player_1': player_1,
            'player_2': player_2,
            'fight': fight,
        }
        if request.method == 'POST':
            # Procesar el movimiento de los jugadores
            player_1_move = request.POST.get('player_1')
            player_2_move = request.POST.get('player_2')
            result = fightFun(player_1_move, player_2_move)
            # Determinar al ganador de la ronda
            winner_match(result, fight_id)
            fight.refresh_from_db()
            context['fight'] = fight

            if fight.status == 'finish':
                return redirect('victory', fight_id=fight_id)

        return render(request, 'combat_area.html', context)
    except (UserModel.DoesNotExist, FightModel.DoesNotExist) as e:
        # Manejar el caso en el que los jugadores o la pelea no existan
        raise Http404("Alguno de los jugadores o la pelea no existe")

# Vista para la página de combate avanzado
def combatAreaUp(request, player_1_id, player_2_id, fight_id):
    try:
        # Obtener los jugadores y la pelea actual
        player_1 = UserModel.objects.get(id=player_1_id)
        player_2 = UserModel.objects.get(id=player_2_id)
        fight = FightModel.objects.get(id=fight_id)
        
        context = {
            'player_1': player_1,
            'player_2': player_2,
            'fight': fight,
        }
        if request.method == 'POST':
            # Procesar el movimiento de los jugadores
            player_1_move = request.POST.get('player_1')
            player_2_move = request.POST.get('player_2')
            result = fightFun2(player_1_move, player_2_move)
            # Determinar al ganador de la ronda
            winner_match(result, fight_id)
            fight.refresh_from_db()
            context['fight'] = fight

            if fight.status == 'finish':
                return redirect('victory', fight_id=fight_id)

        return render(request, 'combat_area_up.html', context)
    except (UserModel.DoesNotExist, FightModel.DoesNotExist) as e:
        # Manejar el caso en el que los jugadores o la pelea no existan
        raise Http404("Alguno de los jugadores o la pelea no existe")

# Vista para la página de victoria
def victory(request, fight_id):
    try:
        # Obtener la pelea actual
        result = FightModel.objects.get(id=fight_id)
        result.rounds -= 1
        result.save()
        return render(request, 'victory.html', {'result': result})
    except FightModel.DoesNotExist:
        # Manejar el caso en el que la pelea no exista
        raise Http404("La pelea no existe")
