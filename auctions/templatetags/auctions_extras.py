from django import template

register = template.Library()

@register.filter(name='current_bid')
def current_bid(listing):
    maxm = listing.starting_bid
    bids = listing.item_bids.order_by('-amount').first()
    if bids is not None:
        maxm = bids.amount
    return maxm
