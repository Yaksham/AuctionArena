from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.IntegerField()
    image = models.URLField(blank=True, default='')

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass