from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# from .models import Artist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup as bs 
import re
from .models import Song,Artist
from .models import Tune,Topsong
from .forms import SongSearchForm
from .models import Wishlist
from django.urls import reverse

from django.conf import settings




def home(request):
    return render(request, 'index.html')








#index
@login_required(login_url='login')
def index(request):
    songs = Song.objects.all()
    artist_id = request.GET.get('artist', '')
    # track_id = 4
    return render(request, 'templates/index.html',{'songs':songs,'artist_id': artist_id})

    
def search_songs(request):
    form = SongSearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']

        results = Song.objects.filter(
            title__icontains=query
        ) | Song.objects.filter(
            artist__name__icontains=query  # Correct lookup for ForeignKey
        )


    return render(request, 'search.html', {'form': form, 'results': results})








def login(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('login')
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Ensure 'username' is retrieved
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username:  # Check if username is missing
            return render(request, "signup.html", {"error": "Username is required"})

        if password1 != password2:
            return render(request, "signup.html", {"error": "Passwords do not match"})

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            # login(request, user)
            return redirect('home')  # Change "home" to your homepage URL name
        except Exception as e:
            return render(request, "signup.html", {"error": str(e)})

    return render(request, "signup.html")



        

    

@login_required(login_url='login')
def logout(request):
        auth.logout(request)
        return redirect('login')
     






def music_player(request,artist_id):
    # artist_id = request.GET.get('artist',   # Get artist ID from URL parameter

    if artist_id:
        songs = Song.objects.filter(artist_id=artist_id)  # Filter songs by artist ID
    else:
        songs = Song.objects.all()  # Show all songs if no filter applied

    artists = Artist.objects.all()  # Get all artists for the filter dropdown

    return render(request, 'player.html', {'songs': songs, 'artists': artists, 'selected_artist': artist_id})

    

    # artists = Artist.objects.all()
    # return render(request, 'artist_list.html', {'artists': artists})

def Artist_list(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    songs = artist.songs.all()  # Fetch songs for this artist
    return render(request, 'index.html', {'artist': artist, 'songs': songs})


def Topsong_list(request, topsong_id):
    topsong =  get_object_or_404(Topsong, id=topsong_id)
    tunes = topsong.songs.all()  # Fetch songs for this artist
    return render(request, 'index.html', {'topsong': topsong, 'tunes': tunes})



def tune_album(request,topsong_id):
    topsong_id = request.GET.get('topsong', '')  # Get artist ID from URL parameter

    if topsong_id:
        tunes = Tune.objects.filter(topsong_id=topsong_id)  # Filter songs by artist ID
    else:
        tunes = Tune.objects.all()  # Show all songs if no filter applied

    topsong = Topsong.objects.all()  # Get all artists for the filter dropdown

    return render(request, 'album.html', {'tunes': tunes, 'topsong': topsong, 'selected_topsong': topsong_id})


 #whislist


 

@login_required
def add_to_wishlist(request, artist_id):
    song = get_object_or_404(Song, id=artist_id)
    Wishlist.objects.get_or_create(user=request.user, song=song)
    return redirect(reverse('music_player', args=[artist_id])) # Change to your desired redirect page


@login_required
def wishlist_page(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})




# def artist_list(request):
#     # Example logic for displaying artists
#     artists = Artist.objects.all()
#     return render(request, 'player.html', {'artists': artists})


 # Assuming this is your model

def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id)
    item.delete()
    return redirect(reverse('wishlist_page'))  # Update this to match your wishlist page URL name


def profile(request):
    return render(request, 'profile.html') 








