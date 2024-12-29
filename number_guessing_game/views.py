from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
# Create your views here.


def guessing_range(request):
    if request.method == 'POST':
        min_number = int(request.POST.get('min_number', 1))
        max_number = int(request.POST.get('max_number', 100))
        if min_number > max_number:
            return render(request, 'select-range.html', {'error_message': 'Min number cannot be greater than max number.'})
        request.session['min_number'] = min_number
        request.session['max_number'] = max_number
        max_try = int(request.POST.get('max_try', 5))
        request.session['max_try'] = max_try
        request.session['current_try'] = 0
        target_number = random.randint(min_number, max_number)
        request.session['target_number'] = target_number
        return HttpResponseRedirect(reverse('guess_number'))
    return render(request, 'select-range.html')


def guess_number(request):
    min_number = request.session.get('min_number', None)
    max_number = request.session.get('max_number', None)
    target_number = request.session.get('target_number', None)
    max_try = request.session.get('max_try', None)
    current_try = request.session.get('current_try', 0)
    message = ''
    finished = False
    nomore_try = False

    if any(value is None for value in [min_number, max_number, target_number, max_try]):
        return HttpResponseRedirect(reverse('guessing_range'))

    if request.method == 'POST':
        guess = int(request.POST.get('guess', 0))
        current_try += 1
        request.session['current_try'] = current_try

        if current_try == max_try and guess != target_number:
            message = 'You have reached the maximum number of attempts.'
            finished = True
            nomore_try = True
        elif guess < target_number:
            message = 'Your guess is too low. Try again.'
        elif guess > target_number:
            message = 'Your guess is too high. Try again.'
        else:
            message = 'Congratulations! You guessed the number.'
            finished = True
    context = {
        'target_number': target_number,
        'min_number': min_number,
        'max_number': max_number,
        'max_try': max_try,
        'current_try': current_try,
        'message': message,
        'finished': finished,
        'nomore_try': nomore_try
    }
    return render(request, 'number-guessing-game.html', context)
