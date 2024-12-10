from django.contrib import admin
from .models import CustomUser, Game, Purchase, PurchaseDetail, PurchaseItem, ShoppingCart,Rating,CartItem, SearchQuery

# Register your models here.
admin.site.register(CustomUser)  # Use CustomUser instead of User
admin.site.register(Game)
admin.site.register(Purchase)
admin.site.register(PurchaseDetail)
admin.site.register(PurchaseItem)
admin.site.register(ShoppingCart)
admin.site.register(Rating)
admin.site.register(CartItem)
admin.site.register(SearchQuery)