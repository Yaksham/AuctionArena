# from xml.etree.ElementTree import Comment
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Listing, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']

class PlaceBid(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {
            'amount': _(''),
        }

class PostComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': _('Post a comment'),
        }