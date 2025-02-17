from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="owner")
    Watchlist = models.ManyToManyField(User, related_name="auction", blank=True)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=False)
    imageURL = models.TextField(blank=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,related_name="categories")
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True,related_name="bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="buyer")
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True,related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="commentor")
    comment = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="watchlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True,related_name="watchlist")