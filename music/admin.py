from django.contrib import admin

from .models import Mood, Genre, Album, LikeToAlbum, Playlist, Track, TrackInPlaylist

admin.site.register(Mood)
admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(LikeToAlbum)
admin.site.register(Playlist)
admin.site.register(Track)
admin.site.register(TrackInPlaylist)
