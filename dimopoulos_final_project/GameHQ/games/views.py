from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from games_db.models import Game, Rating
from core.views import is_employee
from django.db import transaction
from django.db import connection
from django.db.models import Q
from django.http import Http404
from urllib.parse import unquote

@login_required
def rate_game(request, game_id):
    if request.method == "POST":
        try:
            # Fetch the game object using game_id as the primary key
            game = get_object_or_404(Game, game_id=game_id)
            
            # Get the star rating
            stars = int(request.POST.get('stars', 0))  # Ensure stars is an integer

            # Validate the star rating
            if stars < 1 or stars > 5:
                return JsonResponse({'success': False, 'message': 'Invalid star rating.'})

            # Update or create the user's rating
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                game=game,
                defaults={'stars': stars}
            )

            # Update the game's average rating
            game.update_rating()

            # Return a successful response with the updated average rating
            return JsonResponse({
                'success': True,
                'message': 'Rating submitted successfully.',
                'average_rating': game.rating,
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def games_list(request):
    games = Game.objects.all()
    context = {
        'games': games,
        'star_range': range(1, 6),  # Pass a range for 1 to 5
    }
    return render(request, 'games/games.html', context)

def game_detail(request, game_id):
    game = get_object_or_404(Game, game_id=game_id)
    star_range = range(1, 6)
    return render(request, 'games/game_detail.html', {
        'game': game,
        'star_range': star_range
    })

def games(request, genre=None):
    # Get all unique genres
    genres = Game.objects.values_list('genre', flat=True).distinct()
    print("Genres in view:", list(genres))  # Debug

    # Filter games based on the selected genre
    if genre:
        genre = unquote(genre)
        games = Game.objects.filter(genre=genre)
    else:
        games = Game.objects.all()

    context = {
        'games': games,
        'genres': genres,
        'selected_genre': genre,
    }
    return render(request, 'games/games.html', context)

@login_required
def delete_game(request, game_id):
    # Ensure the user belongs to the Employees group
    if not is_employee(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Handle the POST request
    if request.method == 'POST':
        try:
            game = get_object_or_404(Game, game_id=game_id)
            game.delete()
            return JsonResponse({'message': 'Game deleted successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # If not POST, return an error response
    return JsonResponse({'error': 'Invalid request method.'}, status=400)