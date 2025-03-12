from django.urls import path,include
from .import views
# from .views import tune_album
# from .views import upload_song, song_list
 
urlpatterns = [
    path('',views.index, name='index'),
    path('login/',views.login , name='login'),
    path('signup/',views.signup , name='signup'),
    path('logout',views.logout ,name='logout'),
    path('music/<str:pk>/', views.music, name='music'),
    # path('profile/<str:pk>/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('player/',views.music_player,name='music_player'), 
    path('album/',views.tune_album, name='tune_album'),






]


   
    # path('artistsong',views.artist_song,name='artist_song')
    #  path("upload/", upload_song, name="upload_song"),
    # path("songs/", song_list, name="song_list"),
    
