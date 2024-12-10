from django.contrib import admin
from django.urls import include, path
from home.views import index  # Import the index view
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # URL for login page
    path('signup/', views.signup_view, name='signup'),  # URL for signup page
    path('', index, name='home'),  # Home page URL, referencing the index view
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]