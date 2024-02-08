from django.shortcuts import render, redirect
from .models import UserModel, FightModel
from .utils import fightFun, fightFun2, winner_match

# Create your views here.
def home(request):
    return render(request, 'home.html')

def coliseum(request):
    if request.method == 'POST':
        name_1 = request.POST.get('name_1')
        last_name_1 = request.POST.get('last_name_1')
        name_2 = request.POST.get('name_2')
        last_name_2 = request.POST.get('last_name_2')
        player_1 = UserModel(name = name_1, last_name = last_name_1)
        player_2 = UserModel(name = name_2, last_name = last_name_2)
        player_1.save()
        player_2.save()
        new_fight = FightModel(user_1=player_1, user_2=player_2)
        new_fight.save()
        up_level = request.POST.get('up_level', False)
        if up_level:
            return redirect('combat_area_up', player_1_id=player_1.id, player_2_id=player_2.id, fight_id=new_fight.id)
        return redirect('combat_area', player_1_id=player_1.id, player_2_id=player_2.id, fight_id=new_fight.id)
    return render(request, 'coliseum.html')

def tryAgain(request, result):
    last_fight = FightModel.objects.get(id=result)
    player_1_id = last_fight.user_1_id
    player_1 = UserModel.objects.get(id=player_1_id)
    player_2_id= last_fight.user_2_id
    player_2 = UserModel.objects.get(id=player_2_id)
    new_fight = FightModel(user_1=player_1, user_2=player_2)
    new_fight.save()
    return redirect('combat_area', player_1_id=player_1.id, player_2_id=player_2.id, fight_id=new_fight.id)



def combatArea(request, player_1_id, player_2_id, fight_id):
    player_1 = UserModel.objects.get(id=player_1_id)
    player_2 = UserModel.objects.get(id=player_2_id)
    fight = FightModel.objects.get(id=fight_id)
    
    context = {
        'player_1': player_1,
        'player_2': player_2,
        'fight': fight,
    }
    if request.method == 'POST':
        player_1_move = request.POST.get('player_1')
        player_2_move = request.POST.get('player_2')
        result = fightFun(player_1_move, player_2_move)
        winner_match(result, fight_id)
        fight.refresh_from_db()
        context['fight'] = fight

        if fight.status == 'finish':
            return redirect('victory', fight_id=fight_id)

    return render(request, 'combat_area.html', context)

def combatAreaUp(request, player_1_id, player_2_id, fight_id):
    player_1 = UserModel.objects.get(id=player_1_id)
    player_2 = UserModel.objects.get(id=player_2_id)
    fight = FightModel.objects.get(id=fight_id)
    
    context = {
        'player_1': player_1,
        'player_2': player_2,
        'fight': fight,
    }
    if request.method == 'POST':
        player_1_move = request.POST.get('player_1')
        player_2_move = request.POST.get('player_2')
        result = fightFun2(player_1_move, player_2_move)
        winner_match(result, fight_id)
        fight.refresh_from_db()
        context['fight'] = fight

        if fight.status == 'finish':
            return redirect('victory', fight_id=fight_id)

    return render(request, 'combat_area_up.html', context)

def victory(request, fight_id):
    result = FightModel.objects.get(id=fight_id)
    result.rounds -=1
    result.save()
    return render(request, 'victory.html', {'result' : result})

