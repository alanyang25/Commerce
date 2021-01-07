from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
from .forms import *

def index(request):
    listings = Listing.objects.filter(published = True)

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

def create(request):
    form = ListingModelForm()
    current_user = request.user
    
    # POST method: submit the form
    if request.method == 'POST':
        form = ListingModelForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            current_price = form.cleaned_data['current_price']
            image_link = form.cleaned_data['image_link']
            creater = current_user
            date_time = datetime.datetime.now() 
            published = True
            l = Listing(title=title, category=category, description=description, current_price=current_price,
            image_link=image_link, created_by=creater, published = published)
            l.save()       
        return HttpResponseRedirect(reverse("index"))

    # GET method: show blank form
    return render(request, "auctions/create.html", {
        'form': form
    })

def listing(request, item_n):
    listing = Listing.objects.get(id=item_n)
    form = ListingModelForm(instance=listing)
    bid = BidModelForm()
    comment = CommentModelForm()
    current_user = request.user
    watched = False
    is_pass = None
    close_button = False
    closed = False
    winner = False

    # Add to/Remove from watchlist 
    if listing.watchlist.exists():
        if request.user in listing.watchlist.all():
            watched = True
            if 'remove' in request.GET:
                listing.watchlist.remove(request.user)
                listing.save()
                watched = False
        if 'add' in request.GET:
            listing.watchlist.add(request.user)
            listing.save()
            watched = True
    else:
        if 'add' in request.GET:
            listing.watchlist.add(request.user)
            listing.save()
            watched = True
    # POST form
    if request.method == 'POST':
        # for bid
        if 'submitb' in request.POST:
            bid = BidModelForm(request.POST)
            if bid.is_valid():
                bid.save()
                bidder = current_user
                auction_id = listing
                date_time = datetime.datetime.now()
                bid_price = bid.cleaned_data['bid_price']
                if bid_price > listing.current_price:
                    is_pass = True
                    listing.current_price = bid_price
                    listing.save()
                    b = Bid(bidder=bidder, auction_id=auction_id , bid_time=date_time, bid_price=bid_price)
                    b.save()
                    listing.winner = b.bidder
                    listing.save()
                else:
                    is_pass = False
        # for comment
        elif "submitc" in request.POST:       
            comment = CommentModelForm(request.POST)
            if comment.is_valid():
                commenter = current_user
                auction_id = listing
                date_time = datetime.datetime.now()
                comment_title = comment.cleaned_data['comment_title']
                comment_content = comment.cleaned_data['comment_content']
                c = Comment(commenter=commenter, auction_id=auction_id , comment_time=date_time,
                            comment_title=comment_title, comment_content=comment_content)
                c.save()
                comment = CommentModelForm()
        else:
            comment = CommentModelForm()

    comments = Comment.objects.filter(auction_id=listing)
    comments_count = Comment.objects.filter(auction_id=listing).count()

    # Close bid
    if listing.created_by == current_user:
        close_button = True
        if 'close' in request.GET:
            listing.published = False
            listing.save()
    
    if current_user == listing.winner:
        winner = True
            
    if listing.published == False:
        closed = True   

    return render(request, "auctions/listing.html", {
        'listing': listing,
        'form': form,
        'watched': watched,
        'bid':bid,
        'pass': is_pass,
        'close_button': close_button,
        'closed': closed,
        'winner': winner,
        'comment': comment,
        'comments': comments,
        'comments_count': comments_count
    })

@login_required
def watchlist(request):
    user = request.user
    listings = Listing.objects.filter(watchlist=user)

    return render(request, "auctions/watchlist.html", {
        'listings' : listings,
    })

@login_required
def bid(request):
    return render(request, "auctions/listing.html")

@login_required
def yourlistings(request):
    user = request.user
    listings = Listing.objects.filter(created_by=user)

    return render(request, "auctions/your-listings.html", {
        'listings' : listings,
    })

def categories(request):
    categories = dict(Listing.CATEGORY) # Conversion to a dictionary mapping
    return render(request, "auctions/categories.html", {
        'categories': categories
    })

def category_listing(request, category_name):
    category_listing = Listing.objects.filter(category=category_name)
    return render(request, "auctions/category_listing.html", {
        'category_listing': category_listing,
        'category_name': category_name
    })
