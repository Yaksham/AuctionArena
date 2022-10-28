from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ListingForm, PlaceBid
from .models import User, Listing, Bid#, Watchlist


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def new_listing(request):
    if request.method == 'GET':
        return render(request, "auctions/new_listing.html", {
            "form": ListingForm()
        })
    else:
        form = ListingForm(request.POST)
        listing = form.save(commit=False)
        listing.creator = request.user
        listing.save()
        return redirect("index")


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    maxm = None
    # bids = Bid.objects.filter(listing=listing).order_by('-amount').first()
    bids = listing.item_bids.order_by('-amount').first()
    if bids is not None:
        maxm = bids.amount

    if request.method == 'POST' and 'add' in request.POST:
        listing.watchlisted_by.add(request.user)
        listing.save()
    if request.method == 'POST' and 'remove' in request.POST:
        listing.watchlisted_by.remove(request.user)
        listing.save()

    items = request.user.watched_listings.all()
    watched = listing in items

    if request.method == 'POST':
        form = PlaceBid(request.POST)
        if form.is_valid():
            if maxm is not None:
                if form.cleaned_data['amount'] <= maxm:
                    return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "maxm": maxm,
                    "form": PlaceBid(),
                    "watched": watched,
                    "error": "Bid must be greater than current bid."
                    })
            elif form.cleaned_data["amount"] < listing.starting_bid:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "maxm": maxm,
                    "form": PlaceBid(),
                    "watched": watched,
                    "error": "Bid must be at least equal to the starting bid."
                    })
            maxm = form.cleaned_data['amount']
            bid = form.save(commit=False)
            bid.listing = listing
            bid.bidder = request.user
            bid.save()
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "maxm": maxm,
            "form": PlaceBid(),
            "watched": watched
        })
    

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
