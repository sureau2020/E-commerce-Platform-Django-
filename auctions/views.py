from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Auction, Bid, Comment, Category,Watchlist


def index(request):
    for auction in Auction.objects.filter(state=True):
        for bid in Bid.objects.all():
            if bid.auction == auction and bid.bid_price> auction.current_price:
                auction.current_price = bid.bid_price
                auction.save()
            else:
                pass
    
    return render(request, "auctions/index.html",{
        "Auctions": Auction.objects.filter(state=True),
    })

def watchinglist_view(request):
    if request.user.is_authenticated:
        user = request.user
        watchlists = Watchlist.objects.filter(user=user)
        for auction in Auction.objects.filter(state=True):
            for bid in Bid.objects.all():
                if bid.auction == auction and bid.bid_price> auction.current_price:
                    auction.current_price = bid.bid_price
                    auction.save()
                else:
                    pass
        return render(request, "auctions/watchinglist.html",{
            "watchlists": watchlists
        })
    else:
        return render(request, "auctions/login.html", {
            "message": "To access watching list, you need to login."
        })

def categories_view(request):
    return render(request, "auctions/categories.html",{
        "Categories": Category.objects.all(),
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


def createitme(request):

    if request.method == "POST":
        
        if request.user.is_authenticated:
            user = request.user
        else:
            return render(request, "auctions/createlisting.html", {
                "message": "You must be logged in to create a listing.",
                "Categoryies": Category.objects.all(),
            })        
        try:
            starting_price = float(request.POST["price"])
        except ValueError:
            return render(request, "auctions/createlisting.html", {
                "message": "Please enter a number for the starting price.",
                "Categoryies": Category.objects.all(),
            })
        title = request.POST["title"]
        description = request.POST["describe"]
        categories = Category.objects.get(name=request.POST["category"])
        imageURL = request.POST["imgurl"]

        if starting_price< 0 :
            return render(request, "auctions/createlisting.html", {
                "message": "The starting price can't be smaller than 0.",
                "Categoryies": Category.objects.all(),
            })
        else:
            auction = Auction(user= user, name=title, description= description, imageURL= imageURL, categories= categories, start_price= starting_price, current_price= starting_price)
            auction.save()
            return render(request, "auctions/index.html", {
                "message": "Auction created successfully.",
                "Auctions": Auction.objects.all(),
            })
    else:
        if request.user.is_authenticated:
            return render (request, "auctions/createlisting.html",{
                "Categoryies": Category.objects.all(),
            })
        else:
            return render (request, "auctions/createlisting.html",{
                "message": "You must be logged in to create a listing.",
                "Categoryies": Category.objects.all(),
            })
    

def BID(request):
    if request.method == "POST":
        id= request.POST["auction"]
        auction = Auction.objects.get(id= id)
        try:
            bid_price = float(request.POST["price"])
            
        except ValueError:
            return render(request, "auctions/404.html",{
                "message": "The bid price must be a number.",
                "auction":auction,
            })
        if bid_price <= auction.current_price:
            return render(request, "auctions/404.html",{
                "message": "The bid price must be bigger than current price.",
                "auction":auction,
            })
        else:
            user = User.objects.get(username= request.POST["user"])
            bid = Bid(user= user, auction= auction, bid_price= bid_price)
            bid.save()
            return HttpResponseRedirect(reverse('auction',args=(id,)))


def auction_view(request, auction_id):
    try:
        auction = Auction.objects.get(id=auction_id)
    except Auction.DoesNotExist:
        return render(request, "auctions/index.html",{
            "message": "The auction you want to see does not exist.",
            "Auctions": Auction.objects.all(),
        })
    for bid in Bid.objects.all():
            if bid.auction == auction and bid.bid_price> auction.current_price:
                auction.current_price = bid.bid_price
                auction.save()
    comments = Comment.objects.filter(auction=auction)

    tmp = Bid.objects.filter(auction=auction)

    stateAuction = auction.state

    ownerState = False
    watchlistState = False
    bids = Bid.objects.filter(auction=auction).order_by('-time')

    if tmp.count() > 0:
        last_bid = Bid.objects.filter(auction=auction).last()

        if request.user.is_authenticated:
            user = request.user
            if auction.user == user:
                ownerState = True
            else:
                pass
            ExistOfW = Watchlist.objects.filter(user=user,auction=auction)
            if ExistOfW.count() > 0 :
                watchlistState = True
            else:
                pass
            return render(request, "auctions/auction.html",{
                "bid": last_bid,
                "bids":bids,
                "auction": auction,
                "user": user,
                "comments": comments,
                "owner":ownerState,
                "watchlist":watchlistState,
                "opened":stateAuction,
            })
        else:
            return render(request, "auctions/auction.html",{
                "bid": last_bid,
                "bids":bids,
                "auction": auction,
                "comments": comments,
                "opened":stateAuction,
                "watchlist":watchlistState,
            })
    else:
        if request.user.is_authenticated:
            user = request.user
            if auction.user == user:
                ownerState = True
            else:
                pass
            ExistOfW = Watchlist.objects.filter(user=user,auction=auction)
            if ExistOfW.count() > 0 :
                watchlistState = True
            else:
                pass
            return render(request, "auctions/auction.html",{
                "auction": auction,
                "user": user,
                "bids":bids,
                "comments": comments,
                "owner":ownerState,
                "watchlist":watchlistState,
                "opened":stateAuction,
            })
        else:
            return render(request, "auctions/auction.html",{
                "auction": auction,
                "bids":bids,
                "comments": comments,
                "opened":stateAuction,
                "watchlist":watchlistState,
            })
    
    
def category(request, category_name):
    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        return render(request, "auctions/categories.html",{
            "message": "Category you are looking for does not exist.  All categories:",
            "Categories": Category.objects.all(),
            })
    auctions = Auction.objects.filter(categories=category,state=True)
    if auctions.count() >0:
        return render(request, "auctions/category.html",{
            "auctions": auctions,
            "category": category,
        })
    else:
        return render(request, "auctions/category.html",{
            "category": category,
            "message": "There are no items in this category.",
        })
    
def comment(request):
    if request.method == "POST":
        auction_id = request.POST["auction_id"]
        auction = Auction.objects.get(id=auction_id)
        content = request.POST["content"]
        user = request.user
        comment = Comment(auction=auction, comment=content,user=user)
        comment.save()
        return HttpResponseRedirect(reverse('auction',args=auction_id))
            

def watchlist_add(request,auction_id):
    id= auction_id
    auction = Auction.objects.get(id=auction_id)
    user = request.user
    watched = Watchlist(auction=auction,user=user)
    watched.save()
    return HttpResponseRedirect(reverse('auction',args=(id,)))
    

def auction_close(request, auction_id):
    id= auction_id
    auction = Auction.objects.get(id=auction_id)
    auction.state = False
    auction.save()
    return HttpResponseRedirect(reverse('auction',args=(id,)))

def watchlist_remove(request, auction_id):
    id= auction_id
    auction = Auction.objects.get(id=auction_id)
    user = request.user
    watched = Watchlist.objects.filter(auction=auction,user=user)
    watched.delete()
    return HttpResponseRedirect(reverse('auction',args=(id,)))

