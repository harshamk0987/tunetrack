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





from django.conf import settings




def home(request):
    return render(request, 'index.html')





def top_artists():
    url = "https://spotify-scraper.p.rapidapi.com/v1/chart/artists/top"





    headers = {
	    "x-rapidapi-key": "91a51b85fbmshafa1c02062b63ebp1e23ecjsn46985782d383",
	    "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"

        }
    response = requests.get(url, headers=headers)

    response_data =response.json()

    artists_info =[]

    if 'artists' in response_data:
        for artist in response_data['artists']:
            name=artist.get('Name','No Name')
            avatar_url = artist.get('visuals',{}).get('avatar',[{}][0].get('url','No URL'))
            artist_id = artist.get('Id','No Id')
            artists_info.append((name,avatar_url,artist_id))
    return artists_info


def top_tracks():
    url = "https://spotify-scraper.p.rapidapi.com/v1/chart/tracks/top"


    headers = {
	"x-rapidapi-key": "91a51b85fbmshafa1c02062b63ebp1e23ecjsn46985782d383",
	"x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)


    data = response.json()
    track_details = []






    if 'tracks' in data:
        shortened_data = data['tracks'][:18]

        # id, name, artist, cover url 
        for track in shortened_data:
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name'] if track['artists'] else None
            cover_url = track['album']['cover'][0]['url'] if track['album']['cover'] else None

            track_details.append({
                'id': track_id,
                'name': track_name,
                'artist': artist_name,
                'cover_url': cover_url
            })


        else:
            print("track not foun in response")

    return track_details
def get_audio_etails(query):

    url = "https://spotify-scraper.p.rapidapi.com/v1/track/download"

    querystring = {"track": query}

    headers = {
        "X-RapidAPI-Key": "02912db996msh068b089c778126bp13a9d9jsn380afeb7d573",
        "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    audio_details = []

    if response.status_code == 200:
        response_data = response.json()


   

def get_track_image(track_id, track_name):
    url = 'https://open.spotify.com/track/'+track_id
    r = requests.get(url)
    soup = bs(r.content)
    image_links_html = soup.find('img', {'alt': track_name})
    if image_links_html:
        image_links = image_links_html['srcset']
    else:
        image_links = ''

    match = re.search(r'https:\/\/i\.scdn\.co\/image\/[a-zA-Z0-9]+ 640w', image_links)

    if match:
        url_640w = match.group().rstrip(' 640w')
    else:
        url_640w = ''

    return url_640w


    #music

def music(request, pk):

    track_id = pk

    url = "https://spotify-scraper.p.rapidapi.com/v1/track/metadata"

    querystring = {"trackId": track_id}

    headers = {
        "X-RapidAPI-Key": "02912db996msh068b089c778126bp13a9d9jsn380afeb7d573",
        "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()

        track_name = data.get("name")
        artists_list = data.get("artists", [])
        first_artist_name = artists_list[0].get("name") if artists_list else "No artist found"

        audio_details_query = track_name + first_artist_name
        audio_details = get_audio_etails(audio_details_query)
        audio_url = audio_details[0]
        duration_text = audio_details[1]

        track_image = get_track_image(track_id, track_name)

        context = {
            'track_name': track_name,
            'artist_name': first_artist_name,
            'audio_url': audio_url,
            'duration_text': duration_text,
            'track_image': track_image,
        }

    return render(request,'music.html', context )




#index
@login_required(login_url='login')
def index(request):
    songs = Song.objects.all()
    artist_id = request.GET.get('artist', '')
    # track_id = 4
    return render(request, 'templates/index.html',{'songs':songs,'artist_id': artist_id})

    
    
    # return render(request,'index.html')


#search





# def search_songs(request):
#     form = SongSearchForm(request.GET)
#     results = []

#     if form.is_valid():
#         query = form.cleaned_data['query']
#         results = Song.objects.filter(
#             title__icontains=query
#         ) | Song.objects.filter(
#             artist__icontains=query
#         ) | Song.objects.filter(
#             album__icontains=query
#         )

#     return render(request, 'search.html', {'form': form, 'results': results})
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


# def search_songs(request):
#     query = request.GET.get('q')
#     songs = Song.objects.filter(title__icontains=query) if query else Song.objects.all()

#     return render(request, 'templates/search.html', {'songs': songs, 'query': query})
    



    # if request.method == 'POST':
    #     search_query = request.POST['search_query']

    #     url = "https://spotify-scraper.p.rapidapi.com/v1/search"

    #     querystring = {"term":search_query,"type":"track"}

    #     headers = {
    #         "X-RapidAPI-Key": "02912db996msh068b089c778126bp13a9d9jsn380afeb7d573",
    #         "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
    #     }

    #     response = requests.get(url, headers=headers, params=querystring)

    #     track_list = []

    #     if response.status_code == 200:
    #         data = response.json()

    #         search_results_count = data["tracks"]["totalCount"]
    #         tracks = data["tracks"]["items"]

    #         for track in tracks:
    #             track_name = track["name"]
    #             artist_name = track["artists"][0]["name"]
    #             duration = track["durationText"]
    #             trackid = track["id"]

    #             if get_track_image(trackid, track_name):
    #                 track_image = get_track_image(trackid, track_name)
    #             else:
    #                 track_image = "https://imgv3.fotor.com/images/blog-richtext-image/music-of-the-spheres-album-cover.jpg"

    #             track_list.append({
    #                 'track_name': track_name,
    #                 'artist_name': artist_name,
    #                 'duration': duration,
    #                 'trackid': trackid,
    #                 'track_image': track_image,
    #             })
    #     context = {
    #         'search_results_count': search_results_count,
    #         'track_list': track_list,
    #     }

    #     return render(request, 'search.html', context)
    # else:
    #     return render(request, 'search.html')
    





    









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
            login(request, user)
            return redirect("home")  # Change "home" to your homepage URL name
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
def wishlist_view(request):
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
    return redirect('wishlist_page')  # Update this to match your wishlist page URL name







