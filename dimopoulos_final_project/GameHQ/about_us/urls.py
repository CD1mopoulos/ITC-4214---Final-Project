from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about_us, name='about_us'),
]
