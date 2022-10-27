from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']

class PlaceBid(forms.Form):
    bid = forms.IntegerField(label='Place Bid', step_size=1)