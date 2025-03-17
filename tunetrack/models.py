from django.db import models
from django.contrib.auth.models import User
 # Assuming this is your model





class Artist(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='top_artist/',null=True, blank=True)

    def __str__(self):
        return self.name
    



class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")
    # artist = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True, null=True)
    # audio_url = models.CharField(max_length=255, default='default_audio.mp3')
    audio_url = models.FileField(upload_to='audio/')
    duration = models.IntegerField(null=True, blank=True)

    cover_image = models.ImageField(upload_to="cover_images/", blank=True, null=True)

    def __str__(self):
        return self.title
    

    




class Topsong(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='Topsong/',null=True, blank=True)

    def __str__(self):
        return self.name
    


class Tune(models.Model):
    title = models.CharField(max_length=255)
    topsong = models.ForeignKey(Topsong, on_delete=models.CASCADE, related_name="tunes")
    # artist = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True, null=True)
    # audio_url = models.CharField(max_length=255, default='default_audio.mp3')
    audio_url = models.FileField(upload_to='audio/')
    duration = models.IntegerField(null=True, blank=True)

    cover_image = models.ImageField(upload_to="cover_images/", blank=True, null=True)

    def __str__(self):
        return self.title
    


   

# whislist


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'song')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.user.username} - {self.song.title}"
    






