from datetime import time

from django.test import TestCase, Client

from .models import (
    Artist,
    Thumbnail,
    Type,
    Collection,
    Playlist,
    Media
)


class StreamViewTest(TestCase):
    def setUp(self):
        thumbnail = Thumbnail.objects.create(
            url='test_url'
        )

        artist = Artist.objects.create(
            name='test_artist',
            url='test_url',
            thumbnail=thumbnail,
        )

        type = Type.objects.create(
            name='test_type'
        )

        collection = Collection.objects.create(
            name='test_collection',
            thumbnail=thumbnail,
            type=type
        )

        playlist = Playlist.objects.create(
            name='test_playlist',
            artist=artist,
            thumbnail=thumbnail,
            type=type,
            collection=collection
        )

        Media(
            name='ra-mu-ne',
            length=time(minute=5, second=12),
            views=8320,
            url='roses.mp3',
            artist=artist,
            thumbnail=thumbnail,
            type=type,
            collection=collection,
            playlist=playlist
        ).save()

    def test_get_success(self):
        client = Client()
        response = client.get('/music/1')

        self.assertEqual(response.status_code, 200)

    def test_get_404(self):
        client = Client()
        response = client.get('music/56473')

        self.assertEqual(response.status_code, 404)
