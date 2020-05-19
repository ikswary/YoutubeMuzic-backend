from django.db import models
from music.models import (
    Playlist,
    Media,
    Artist
)


class User(models.Model):
    google_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'

class ListStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    playlist = models.ForeignKey(Playlist, on_delete=models.PROTECT)

    class Meta:
        db_table = 'list_storages'

class MediaStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    media = models.ForeignKey(Media, on_delete=models.PROTECT)

    class Meta:
        db_table = 'media_storages'


class RecentPlaylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    playlist = models.ForeignKey(Playlist, on_delete=models.PROTECT)

    class Meta:
        db_table = 'recent_playlists'


class RecentMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    playlist = models.ForeignKey(Playlist, on_delete=models.PROTECT)

    class Meta:
        db_table = 'recent_medias'

class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    media = models.ForeignKey(Media, on_delete=models.PROTECT)
    like_unlike = models.BooleanField()

    class Meta:
        db_table = 'evaluations'

class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)

    class Meta:
        db_table = 'subscribes'

