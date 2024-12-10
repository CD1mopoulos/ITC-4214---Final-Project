from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def games_list(request):
    return render(request, 'games/games.html')

def about_us(request):
    return render(request, 'about_us/aboutUs.html')

def contact(request):
    return render(request, 'contact/contact.html')

def search(request):
    return render(request, 'search/search_page.html')