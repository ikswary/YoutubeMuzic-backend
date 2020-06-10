from django.db    import models

from music.models import (
    Playlist,
    Media,
    Artist
)


class User(models.Model):
    name = ..
    email = ...
    google_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'

class UserPlayList(models.Model):
    user        = models.ForeignKey(User, on_delete     = models.PROTECT)
    playlist    = models.ForeignKey(Playlist, on_delete = models.PROTECT)
    listened_at = models.DateTimeField(auto_now         = True)

    class Meta:
        db_table = 'list_storages'

class UserMedia(models.Model):
    user        = models.ForeignKey(User, on_delete  = models.PROTECT)
    media       = models.ForeignKey(Media, on_delete = models.PROTECT)
    listened_at = models.DateTimeField(auto_now      = True)
    like        = models.BooleanField(null = True)

    class Meta:
        db_table = 'media_storages'

class Subscribe(models.Model):
    user   = models.ForeignKey(User, on_delete   = models.PROTECT)
    artist = models.ForeignKey(Artist, on_delete = models.PROTECT)
    periodic = ...
    price = ..

    class Meta:
        db_table = 'subscribes'
