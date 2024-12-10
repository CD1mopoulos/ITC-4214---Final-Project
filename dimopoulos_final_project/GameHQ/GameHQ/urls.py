"""
URL configuration for GameHQ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Home page app (root)
    path('', include('games.urls')),  # Games page app
    path('', include('about_us.urls')),  # About Us page
    path('', include('contact.urls')),  # Contact page app
    path('', include('games_db.urls')),
    #path('core/', include('core.urls')),  # Core functionality under '/core/'
    path('register/', include('register.urls')),
    path('', include("django.contrib.auth.urls")),
    path('search/', include('search.urls')),
    path('Add_Game/', include('Add_Game.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files during development if in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)