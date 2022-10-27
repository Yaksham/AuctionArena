from django import forms
from .models import Listing, Bid

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']

class PlaceBid(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']