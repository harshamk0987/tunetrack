from django import forms




class SongSearchForm(forms.Form):
    query = forms.CharField(label='Search Songs', max_length=100)

# from .models import Song

# class SongUploadForm(forms.ModelForm):
#     class Meta:
#         model = Song
#         fields = ["title", "artist", "album", "genre", "file", "cover_image"]