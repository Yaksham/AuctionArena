from django.contrib import admin
from .models import User, Listing, Bid, Comment

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "creator", "winner")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "listing", "bidder")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "content", "author", "time")

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
