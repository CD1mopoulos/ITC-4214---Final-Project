# views.py in games_db app
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem, Purchase, PurchaseDetail, Game, ShoppingCart, PurchaseItem
from django.core.mail import send_mail
from core.forms import UserSignupForm  # Import the form from the core app
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db import transaction

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user to the User model
            return redirect('home')  # Redirect to a page after successful signup
    else:
        form = UserSignupForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def view_cart(request):
    # Get or create the user's shopping cart
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)

    # Fetch cart items related to this cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate the total price of the items in the cart (if using a total_cost method)
    total_price = cart.total_cost()  # Assuming total_cost is a method in your ShoppingCart model

    # Render the cart template with cart items and total price
    return render(request, 'games_db/cart.html', {
        'cart_items': cart_items,  # List of items in the cart
        'total_price': total_price  # Total price of all items in the cart
    })

#@login_required
#def add_to_cart(request, game_id):
#    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
#    game = Game.objects.get(id=game_id)
#    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=game)
#    if not created:
#        cart_item.quantity += 1
#        cart_item.save()
#    return redirect('view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

def order_complete(request):
    return render(request, 'games_db/order_complete.html')

@login_required
def checkout(request):
    if request.method == 'POST':
        # Create the purchase
        purchase = Purchase.objects.create(user=request.user)
        
        # Get the cart items for the logged-in user
        cart_items = CartItem.objects.filter(cart__user=request.user)
        
        # Calculate the total price of all cart items
        total_price = sum(item.quantity * item.product.price for item in cart_items)
        
        # Create a purchase detail record
        purchase_detail = PurchaseDetail.objects.create(
            purch=purchase,
            name=request.POST['name'],
            surname=request.POST['surname'],
            address=request.POST['address'],
            phone=request.POST['phone'],
            payment_method=request.POST['payment_method'],
            email=request.POST['email']
        )
        
        # Create the purchase items and reduce stock (optional)
        for item in cart_items:
            PurchaseItem.objects.create(
                purch=purchase,
                game=item.product,
                quantity=item.quantity
            )
            # Optionally, reduce the quantity in the `Game` model
            item.product.availability -= item.quantity
            item.product.save()
        
        # Clear the cart after purchase
        cart_items.delete()
        
        return redirect('order_complete')
    
    return render(request, 'games_db/checkout.html')

@login_required
def add_to_cart(request, game_id):
    if request.method == "POST":
        try:
            # Get the product using game_id
            product = get_object_or_404(Game, game_id=game_id)

            # Get or create the cart for the user
            cart, created = ShoppingCart.objects.get_or_create(user=request.user)

            # Get or create the cart item for the product
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

            # If the item already exists in the cart, increment the quantity
            if not item_created:
                cart_item.quantity += 1
                cart_item.save()

            # Calculate the total number of items in the cart
            total_items = sum(item.quantity for item in cart.cart_items.all())

            return JsonResponse({'success': True, 'total_items': total_items})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})