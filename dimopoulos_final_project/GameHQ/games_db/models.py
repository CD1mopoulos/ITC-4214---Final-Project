from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    # Adding the custom 'created' field to track when the user was created
    created = models.DateTimeField(auto_now_add=True)

    # You can add more custom fields here if needed
    # For example, if you want to add a birthday field:
    # birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    pegi = models.IntegerField()  # PEGI rating, assuming integer
    console = models.CharField(max_length=100)
    requirements = models.TextField()
    publisher = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.IntegerField()  # Could be stock count or similar
    photo = models.ImageField(upload_to='game_photos/', blank=True, null=True)
    trailer = models.URLField(blank=True, null=True)
    rel_date = models.DateField()  # Release date
    rating = models.FloatField()  # Rating out of 5 or 10
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('game_detail', args=[self.game_id])

    def update_rating(self):
        # Get all ratings for this game and calculate the average
        ratings = Rating.objects.filter(game=self)
        total_stars = sum([rating.stars for rating in ratings])
        num_ratings = ratings.count()
        
        if num_ratings > 0:
            self.rating = total_stars / num_ratings
        else:
            self.rating = 0  # No ratings yet

        self.save()
        
class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='rating_set', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])  # Star rating (1 to 5)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

class PurchaseDetail(models.Model):
    pd_id = models.AutoField(primary_key=True)
    purch = models.OneToOneField('Purchase', on_delete=models.CASCADE)  # Reference as a string
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"PurchaseDetail {self.pd_id} for Purchase {self.purch.purch_id}"

class Purchase(models.Model):
    purch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    purchase_date = models.DateTimeField(auto_now_add=True)
    purchase_details = models.OneToOneField(PurchaseDetail, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)  # Track if the order is completed

    def __str__(self):
        return f"Purchase {self.purch_id} by {self.user}"


class PurchaseItem(models.Model):
    p_item_id = models.AutoField(primary_key=True)
    purch = models.ForeignKey(Purchase, related_name="purchase_items", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Item {self.p_item_id} for Purchase {self.purch.purch_id} - Game: {self.game.title}"
    

class ShoppingCart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shopping Cart for {self.user.username}"

    def total_cost(self):
        total = 0
        for item in self.cart_items.all():
            total += item.product.price * item.quantity
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in cart"

    def total_price(self):
        return self.product.price * self.quantity

class SearchQuery(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query