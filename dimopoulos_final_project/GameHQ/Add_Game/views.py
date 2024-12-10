from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from games_db.models import Game
from core.views import is_employee
from django.contrib import messages

@login_required
@user_passes_test(is_employee)
def add_game_view(request):
    games = Game.objects.all()

    if request.method == "POST" and "add_game" in request.POST:
        # Collect form data
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        genre = request.POST.get("genre", "").strip()
        pegi = request.POST.get("pegi")
        console = request.POST.get("console", "").strip()
        requirements = request.POST.get("requirements", "").strip()
        publisher = request.POST.get("publisher", "").strip()
        price = request.POST.get("price")
        availability = request.POST.get("availability")
        photo = request.FILES.get("photo")  # Uploaded image
        trailer = request.POST.get("trailer", "").strip()
        rel_date = request.POST.get("rel_date")
        rating = request.POST.get("rating")

        # Check for missing or invalid fields
        if not title or not description or not genre:
            messages.error(request, "Please fill in all required fields.")
            return redirect(request.path)

        try:
            # Create a new Game object
            Game.objects.create(
                title=title,
                description=description,
                genre=genre,
                pegi=pegi,
                console=console,
                requirements=requirements,
                publisher=publisher,
                price=price,
                availability=availability,
                photo=photo,
                trailer=trailer,
                rel_date=rel_date,
                rating=rating,
            )
            messages.success(request, "Game added successfully!")
        except Exception as e:
            messages.error(request, f"Failed to add game: {e}")
        
        return redirect(request.path)  # Refresh the page

    return render(request, "Add_Game/add_games.html", {"games": games})
