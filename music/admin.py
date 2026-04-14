from django.contrib import admin
from .models import Artist, Album, Song, UserPlaylist, User

# Register your models
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(UserPlaylist)

