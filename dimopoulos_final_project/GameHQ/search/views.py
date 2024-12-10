from django.shortcuts import render
from games_db.models import Game, SearchQuery
from django.db import models
from django.db.models import Count

def search_page(request):
    # Get search parameters from the URL
    game_title = request.GET.get('game_title', '')
    publisher = request.GET.get('publisher', '')

    # Track the search query (save it to the database) for logged-in and non-logged-in users
    if game_title or publisher:
        query_string = f"{game_title} {publisher}"

        # Create and save the search query in the database (for authenticated and non-authenticated users)
        SearchQuery.objects.create(user=request.user if request.user.is_authenticated else None, query=query_string)

        # Fetch the games that match the query
        games = Game.objects.all()
        if game_title:
            games = games.filter(title__icontains=game_title)
        if publisher:
            games = games.filter(publisher__icontains=publisher)

        # Find the genre of the first game in the search result (if any)
        genre = None
        if games.exists():
            genre = games.first().genre
        
        # Recommend games with the same genre (excluding the current search results)
        recommended_games = []
        if genre:
            recommended_games = Game.objects.filter(genre=genre).exclude(game_id__in=games.values_list('game_id', flat=True))[:5]

    else:
        games = []
        recommended_games = []

    # Fetch the most searched games (all users' search queries aggregated by count)
    most_searched_games = SearchQuery.objects.values('query')\
        .annotate(count=Count('query'))\
        .order_by('-count')[:10]

    # Get the games that correspond to the most searched queries
    most_searched_game_objects = []
    for entry in most_searched_games:
        query_string = entry['query']
        search_terms = query_string.split()  # Split the query string into terms (game title, publisher)
        
        # Look for games that match any of these search terms
        for term in search_terms:
            matching_games = Game.objects.filter(title__icontains=term)
            most_searched_game_objects.extend(matching_games)

    # Remove duplicates if any
    most_searched_game_objects = list(set(most_searched_game_objects))

    # Fetch the user's search history if the user is logged in
    user_search_history = []
    if request.user.is_authenticated:
        # Get the search history of the user
        user_search_queries = SearchQuery.objects.filter(user=request.user).order_by('-timestamp')[:10]
        
        # Extract games associated with the user's search history
        for query in user_search_queries:
            search_terms = query.query.split()  # Split query into terms (game title, publisher)
            for term in search_terms:
                matching_games = Game.objects.filter(title__icontains=term)
                user_search_history.extend(matching_games)

        # Remove duplicates from the search history
        user_search_history = list(set(user_search_history))

    return render(request, 'search/search_page.html', {
        'games': games,
        'recommended_games': recommended_games,
        'most_searched_games': most_searched_game_objects,
        'user_search_history': user_search_history,  # Pass the user's search history to the template
    })
