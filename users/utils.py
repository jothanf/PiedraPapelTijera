from .models import FightModel, UserModel

# Función para determinar el resultado de una ronda de juego
def fightFun(move_1, move_2):
    if move_1 == move_2:
        return 'empate'
    elif (move_1 == 'piedra' and move_2 == 'tijera') or \
         (move_1 == 'papel' and move_2 == 'piedra') or \
         (move_1 == 'tijera' and move_2 == 'papel'):
        return 'player_1'
    else:
        return 'player_2'

# Función alternativa para determinar el resultado de una ronda de juego, con más movimientos
def fightFun2(move_1, move_2):
    if move_1 == move_2:
        return 'empate'
    elif (move_1 == 'tijera' and move_2 == 'papel') or \
         (move_1 == 'papel' and move_2 == 'piedra') or \
         (move_1 == 'piedra' and move_2 == 'lagarto') or \
         (move_1 == 'lagarto' and move_2 == 'spock') or \
         (move_1 == 'spock' and move_2 == 'tijera') or \
         (move_1 == 'tijera' and move_2 == 'lagarto') or \
         (move_1 == 'lagarto' and move_2 == 'papel') or \
         (move_1 == 'papel' and move_2 == 'spock') or \
         (move_1 == 'spock' and move_2 == 'piedra') or \
         (move_1 == 'piedra' and move_2 == 'tijera'):
        return 'player_1'
    else:
        return 'player_2'

# Función para actualizar el estado de la pelea y verificar al ganador
def winner_match(result, fight_id):
    fight = FightModel.objects.get(id=fight_id)

    # Actualizar los contadores de victorias y empates
    if result == "player_1":
        fight.winner_1 += 1
    elif result == "player_2":
        fight.winner_2 += 1
    else:
        fight.tie += 1

    # Incrementar el número de rondas y guardar los cambios
    fight.rounds += 1
    fight.save()
    # Verificar si hay un ganador de la pelea
    check_winner(fight)

# Función para verificar si hay un ganador de la pelea
def check_winner(fight):
    if fight.winner_1 == 3:
        user_1 = UserModel.objects.get(id=fight.user_1_id)
        fight.grand_winner = user_1
        fight.status = 'finish'
    elif fight.winner_2 == 3:
        user_2 = UserModel.objects.get(id=fight.user_2_id)
        fight.grand_winner = user_2
        fight.status = 'finish'
    fight.save()