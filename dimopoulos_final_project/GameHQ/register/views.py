# In register/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from core.forms import UserSignupForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from core.forms import CustomUserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from games_db.models import ShoppingCart, CartItem
import logging
logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)  # Only pass data for POST requests
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the home page after login
        else:
            messages.error(request, "Invalid credentials")  # Show error if credentials are invalid
    else:
        form = UserLoginForm()  # Empty form for GET requests

    # Render the login template from the 'register' app
    return render(request, 'registration/login.html', {'login_form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            # Save the user, hash the password and log them in immediately
            user = form.save()
            login(request, user)  # Log the user in after signup
            messages.success(request, "Account created successfully!")
            return redirect('home')  # Redirect to home page after signup and login
    else:
        form = UserSignupForm()

    return render(request, 'register/signup.html', {'signup_form': form})



@login_required
def logout_view(request):
    try:
        # Fetch the user's shopping cart and delete all items
        cart = ShoppingCart.objects.get(user=request.user)
        cart.cart_items.all().delete()
    except ShoppingCart.DoesNotExist:
        # If no cart exists, do nothing
        pass
    
    # Perform logout
    logout(request)
    
    # Redirect to the home page or any other page
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = CustomUserChangeForm(request.POST, instance=request.user)

        if profile_form.is_valid():
            # Check for password change
            new_password = profile_form.cleaned_data.get("new_password")
            if new_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Keep the user logged in

            # Save other profile details
            profile_form.save()

            # Success message and redirect
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to the same page after the update
        else:
            messages.error(request, "There were errors updating your profile. Please review the form.")

    else:
        profile_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'register/profile.html', {
        'profile_form': profile_form,
    })

