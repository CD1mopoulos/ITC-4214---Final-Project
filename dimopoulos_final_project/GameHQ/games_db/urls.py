# games_db/urls.py
from django.urls import path
from . import views  # Import your views from the games_db app

urlpatterns = [
    # Example URL pattern for the signup view
    path('signup/', views.signup_view, name='signup'),
    # Add other URL patterns as needed
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:game_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_complete/', views.order_complete, name='order_complete'),
    #path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
]
