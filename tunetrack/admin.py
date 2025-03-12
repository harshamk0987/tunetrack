from django.contrib import admin
from .models import  Artist,Song
from .models import Topsong,Tune

# Register your models here.
admin.site.register(Artist)
admin.site.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'duration')


admin.site.register(Topsong)
admin.site.register(Tune)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'Topsong', 'duration')
