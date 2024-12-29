from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
# Create your views here.


def player_settings(request):
    if request.method == 'POST':
        # Reset the game
        request.session.flush()

        # If there's no form data, just redirect to settings page
        if not request.POST.get('player_name'):
            return render(request, 'player-settings.html')

        player_name = request.POST.get('player_name', 'Player')
        winner_score = int(request.POST.get('winner_score', 3))

        # Initialize session variables
        request.session['player_name'] = player_name
        request.session['winner_score'] = winner_score
        request.session['player_score'] = 0
        request.session['computer_score'] = 0
        request.session['game_history'] = []

        return HttpResponseRedirect(reverse('rock_paper_scissors'))

    return render(request, 'player-settings.html')


def rock_paper_scissors(request):
    # Check if game is initialized
    player_name = request.session.get('player_name')
    winner_score = request.session.get('winner_score')

    if not all([player_name, winner_score]):
        return HttpResponseRedirect(reverse('player_settings'))

    CHOICES = {
        'r': {'name': 'Rock', 'emoji': '🪨', 'beats': 's'},
        'p': {'name': 'Paper', 'emoji': '📰', 'beats': 'r'},
        's': {'name': 'Scissors', 'emoji': '✂️', 'beats': 'p'}
    }

    round_result = {}

    # Get current scores
    player_score = request.session.get('player_score', 0)
    computer_score = request.session.get('computer_score', 0)

    # Process player choice
    player_choice = request.GET.get('player_choice')
    computer_choice = random.choice(list(CHOICES.keys())) if player_choice else None

    # Determine winner if choices were made
    if player_choice and computer_choice:
        if player_choice == computer_choice:
            result = "Tie!"
        elif CHOICES[player_choice]['beats'] == computer_choice:
            result = "You win!"
            player_score += 1
            request.session['player_score'] = player_score
        else:
            result = "Computer wins!"
            computer_score += 1
            request.session['computer_score'] = computer_score

        # Store round result
        round_result = {
            'player_choice': CHOICES[player_choice]['emoji'],
            'computer_choice': CHOICES[computer_choice]['emoji'],
            'result': result
        }
        game_history = request.session.get('game_history', [])
        game_history.append(round_result)

        # Check for game over
        if player_score >= winner_score or computer_score >= winner_score:
            final_result = "Congratulations! You won!" if player_score > computer_score else "Game Over! Computer wins!"
            request.session['game_finished'] = True
            request.session['final_result'] = final_result

    context = {
        'player_name': player_name,
        'winner_score': winner_score,
        'player_score': player_score,
        'computer_score': computer_score,
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'round_result': round_result if round_result else None,
        'game_finished': request.session.get('game_finished', False),
        'final_result': request.session.get('final_result', '')
    }

    return render(request, 'rock-paper-scissors.html', context)
