# core/context_processors.py
from core.forms import UserLoginForm
from core.forms import UserSignupForm  # Import your custom signup form

def login_form_context(request):
    return {'login_form': UserLoginForm()}


def signup_form_context(request):
    """Add signup form to context globally"""
    return {
        'signup_form': UserSignupForm()  # Add an instance of the signup form to context
    }
