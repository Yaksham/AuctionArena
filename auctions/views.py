from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ListingForm, PlaceBid, PostComment
from .models import User, Listing, Bid, Comment


def categories(request):
    categories = Listing.objects.values_list('category', flat=True).distinct().order_by('category').filter(winner=None)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category_name):
    listings = Listing.objects.filter(category=category_name, winner=None)
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category_name": category_name
    })


def index(request):
    listings = Listing.objects.filter(winner=None)
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


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    # listing_owner = listing.creator == request.user if listing.winner == '' else listing.winner.username
    listing_owner = False
    maxm = None
    max_bid = listing.item_bids.order_by('-amount').first()
    if max_bid is not None:
        maxm = max_bid.amount

    if request.method == 'POST' and 'close' in request.POST:
        listing.winner = max_bid.bidder
        listing.save()
    if request.method == 'POST' and 'add' in request.POST:
        listing.watchlisted_by.add(request.user)
        listing.save()
    if request.method == 'POST' and 'remove' in request.POST:
        listing.watchlisted_by.remove(request.user)
        listing.save()

    watched = request.user.is_authenticated and listing in request.user.watched_listings.all()
    comments = listing.listing_comments.all()

    if listing.creator == request.user:
        listing_owner = True
    if listing.winner is not None:
        listing_owner = (listing.winner == request.user)

    if request.method == 'POST' and 'bid' in request.POST:
        form = PlaceBid(request.POST)
        if form.is_valid():
            if maxm is not None:
                if form.cleaned_data['amount'] <= maxm:
                    return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "maxm": maxm,
                    "form": PlaceBid(),
                    "comment_form": PostComment(),
                    "comments": comments,
                    "watched": watched,
                    "owner": listing_owner,
                    "error": "Bid must be greater than current bid."
                    })
            elif form.cleaned_data["amount"] < listing.starting_bid:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "maxm": maxm,
                    "form": PlaceBid(),
                    "comment_form": PostComment(),
                    "comments": comments,
                    "watched": watched,
                    "owner": listing_owner,
                    "error": "Bid must be at least equal to the starting bid."
                    })
            maxm = form.cleaned_data['amount']
            bid = form.save(commit=False)
            bid.listing = listing
            bid.bidder = request.user
            bid.save()

    if request.method == 'POST' and 'comment' in request.POST:
        form = PostComment(request.POST)
        comment = form.save(commit=False)
        comment.author = request.user
        comment.listing = listing
        comment.save()
            
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "maxm": maxm,
            "form": PlaceBid(),
            "comment_form": PostComment(),
            "comments": comments,
            "watched": watched,
            "owner": listing_owner
        })


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

def watchlist(request):
    list = request.user.watched_listings.all()
    if not len(list):
        list = None
    return render(request, "auctions/watchlist.html", {
        "list": list
    })