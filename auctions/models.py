from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.IntegerField()
    image = models.URLField(blank=True, default='')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.CharField(max_length=64)
    winner = models.ForeignKey(User, blank=True, null=True, default='', on_delete=models.CASCADE, 
    related_name="wins")

class Bid(models.Model):
    amount = models.IntegerField()
    time = models.DateTimeField(default=django.utils.timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_bids")
    bidder = models.ForeignKey(User, related_name="user_bids", on_delete=models.CASCADE)
