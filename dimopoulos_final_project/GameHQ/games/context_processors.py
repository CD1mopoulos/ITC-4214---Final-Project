from games_db.models import Game

def genre_context(request):
    genres = Game.objects.values_list('genre', flat=True).distinct()
    return {
        'genres': genres,
        'selected_genre': request.resolver_match.kwargs.get('genre') if request.resolver_match else None,
    }

def star_range_context(request):
    return {
        'star_range': range(1, 6)  # Makes this range available globally
    }