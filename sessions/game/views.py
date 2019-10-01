from django.shortcuts import render

from .models import Player, Game, PlayerGameInfo
from .forms import ChooseNumberForm


def show_home(request):
    context = {}
    player_pk = request.session.get('player_pk', None) # проверить есть ли игрок

    if player_pk is None: # создать игрока, если отсутствует
        player = Player.objects.create()
        request.session['player_pk'] = player.pk
    else:
        player = Player.objects.get(pk=player_pk) # получить игрока, если уже создан

    game = Game.objects.order_by('-id').first() # попытаться получить существующую игру

    if game is not None and game.is_ended: # если игра есть, но еще не завершена - получить ее информацию
        player_game_info = PlayerGameInfo.objects.filter(game=game).exclude(player=player).first()

        if player_game_info is not None: # получить количество сделанных попыток
            counter = player_game_info.counter

            if counter > 0:
                context['ending_message'] = f'Ваше число угадали с {counter} попытки'

    if game is None or game.is_ended:  # если игры нет
        if request.method == 'GET':  # отрендерить форму для загадывания числа
            context['form'] = ChooseNumberForm()
            context['gamestart'] = True
            return render(
                request,
                'home.html',
                context
            )

        if request.method == 'POST':  # начать игру с полученным числом
            form = ChooseNumberForm(request.POST)

            if form.is_valid():
                game = Game(number=int(form.cleaned_data['number']))
                game.save()
                PlayerGameInfo.objects.create(player=player, game=game, is_master=True)

    player_game_info = PlayerGameInfo.objects.get_or_create(player=player, game=game)[0]

    if player_game_info.is_master:  # вернуть статус игры загадывающему
        context['is_master'] = True
        context['number_message'] = f'Загаданное число: {game.number}'
        context['message'] = 'Второй игрок будет пытаться отгадать его'

    else:  # вернуть статус отгадывающему (и принять вариант на проверку)
        context['form'] = ChooseNumberForm()

        if request.method == 'POST':
            form = ChooseNumberForm(request.POST)

            if form.is_valid():
                user_number = int(form.cleaned_data['number'])
                player_game_info.counter += 1
                player_game_info.save()

                if user_number > game.number:
                    context['message'] = f'Загаданное число меньше {user_number}'
                elif user_number < game.number:
                    context['message'] = f'Загаданное число больше {user_number}'
                else:
                    context['message'] = 'Вы угадали число!'
                    game.is_ended = True
                    game.save()

    return render(
        request,
        'home.html',
        context
    )
