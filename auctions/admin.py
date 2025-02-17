from django.contrib import admin
from .models import User, Auction, Bid, Comment, Category, Watchlist

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist)
# Register your models here.
