from django.urls import path,include
from .import views
from .views import add_to_wishlist

 
urlpatterns = [
    path('home/', views.home, name='home'),
    path('',views.index, name='index'),
    path('login/',views.login , name='login'),
    path('signup/',views.signup , name='signup'),
    path('logout',views.logout ,name='logout'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_songs, name='search_songs'),
    path('player/<int:artist_id>/',views.music_player,name='music_player'), 
    path('album/<int:topsong_id>/', views.tune_album, name='tune_album'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
    path('wishlist/add/<int:artist_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    # path('wishlist/add/song/<int:topsong_id>/', views.add_to_wishlist, name='add_song_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

   
]










   
   
