from datetime import time

from django.test import TestCase, Client

from django.db.models import F

from .models          import (
    Collection,
    Playlist,
    Media,
    Artist,
    Type,
    Thumbnail,
    Hotlist
)

clnt = Client()


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


class MainViewTest(TestCase):
    BASIC_COLLECTION_IDS = [1, 7, 13]
    FIRST_PAGINATION_IDS = clnt.get('/music/main').json()['range_list'][:3]
    FIRST_PAGINATION_URL = '/music/main?collection_id={}&collection_id={}&collection_id={}'.format(
        *FIRST_PAGINATION_IDS)

    def test_first_req_contents(self):
        self.assertEqual(clnt.get('/music/main').json()['contents'],[{
            'collection':Collection.objects.filter(id=i).values('name').first()['name'],
            'elements':list(
                Collection.objects.prefetch_related('playlist_set').filter(id=i).annotate(
                    list_id     = F('playlist__id'),
                    list_name   = F('playlist__name'),
                    list_thumb  = F('playlist__thumbnail_id__url'),
                    list_type   = F('playlist__type_id__name'),
                    list_artist = F('playlist__artist')
                ).values(
                    'list_id',
                    'list_name',
                    'list_thumb',
                    'list_type',
                    'list_artist'))
        } for i in self.BASIC_COLLECTION_IDS])

    def test_first_req_infra_elements(self):
        res = clnt.get('/music/main')

        self.assertEqual(
            res.json()['main_thumb'],
            Collection.objects.filter(id = 1).values('thumbnail_id__url').first()['thumbnail_id__url']
        )
        self.assertTrue(res.json()['range_list'])

    def test_paginate_req_contents_length(self):
        res = clnt.get(self.FIRST_PAGINATION_URL)

        self.assertEqual(
            len(res.json()['contents']),
            3)

    def test_paginate_req_unexpected_keys(self):
        res = clnt.get(self.FIRST_PAGINATION_URL)

        def for_test():
            try:
                res.json()['main_thumb']
                res.json()['range_list']

                return True

            except KeyError:
                return False

        self.assertFalse(for_test())


class ListViewTest(TestCase):
    def setUp(self):
        thumbnail = Thumbnail.objects.create(url = 'github.com/ensia96')

        artist = Artist.objects.create(
            name        = '춤추는망고',
            description = '슈퍼개발자!',
            thumbnail   = thumbnail
        )
        collection = Collection.objects.get(id=13)

        self.playlist = Playlist.objects.create(
            name        = 'haha',
            description = 'this is entity for test!',
            year        = '3030',
            artist      = '춤추는망고',
            thumbnail   = thumbnail,
            type        = Type.objects.get(id=5),
            collection  = collection
        )
        self.media = Media.objects.create(
            name       = '슈퍼망고의 개발자 도전기',
            length     = '6:25',
            album      = '망고의 추억의 앨범',
            artist     = artist,
            thumbnail  = thumbnail,
            collection = collection,
            playlist   = self.playlist
        )

    def test_status_code(self):
        self.assertEqual(clnt.get(f'/music/list/{self.playlist.id}').status_code,200)

        self.assertEqual(clnt.get('/music/list/').status_code,404)

        self.assertEqual(clnt.get('/music/list/a').status_code,404)

    def test_payload_check(self):
        playlist = Playlist.objects.filter(id=self.playlist.id).prefetch_related('media_set')

        self.assertEqual(
            clnt.get(f'/music/list/{self.playlist.id}').json(),
            {'list_meta':{
                'list_name':'haha',
                'list_desc':'this is entity for test!',
                'list_artist':'춤추는망고',
                'list_year':'3030',
                'list_thumb':'github.com/ensia96',
                'list_type':'싱글'
            },'elements':[{
                'item_id':self.media.id,
                'item_thumb':'github.com/ensia96',
                'item_name':'슈퍼망고의 개발자 도전기',
                'item_artist':'춤추는망고',
                'item_album':'망고의 추억의 앨범',
                'item_length':'6:25'
            }]})

