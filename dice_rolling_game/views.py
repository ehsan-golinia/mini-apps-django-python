from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
# Create your views here.


def select_dice(request):
    if request.method == 'POST':
        dice_count = int(request.POST.get('dice_count', 1))
        request.session['dice_count'] = dice_count
        request.session['roll_time'] = 0
        return HttpResponseRedirect(reverse('roll_dice'))
    return render(request, 'select-dice.html')


def dice_rolling_game(request):
    dice_count = request.session.get('dice_count', None)
    roll_time = request.session.get('roll_time', 0)
    if dice_count is None:
        return HttpResponseRedirect(reverse('select_dice'))

    dice_values = [1] * dice_count  # Default values

    if request.method == 'POST':
        # Generate random numbers for all dice
        dice_values = [random.randint(1, 6) for _ in range(dice_count)]
        roll_time += 1
        request.session['roll_time'] = roll_time

    context = {
        'dice_values': dice_values,
        'total': sum(dice_values),
        'range_dice': range(dice_count),
        'roll_time': roll_time
    }
    return render(request, 'dice-rolling-game.html', context)
