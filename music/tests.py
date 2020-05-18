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

    def test_first_req_contents(self):

        res = clnt.get('/music/main')

        self.assertEqual(
            res.status_code,
            200
        )

        self.assertEqual(
            res.json()[
                'contents'
            ],
            [
                {
                    'collection':Collection.objects
                    .filter(
                        id=i
                    ).values(
                        'name'
                    ).first()[
                        'name'
                    ],
                    'elements':
                    list(
                        Collection.objects.prefetch_related(
                            'playlist_set'
                        ).filter(
                            id=i
                        ).annotate(
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
                            'list_artist'
                        )
                    )
                }
                for i in [1,7,13]
            ]
        )



    def test_first_req_infra_elements(self):

        res = clnt.get('/music/main')

        self.assertEqual(
            res.json()[
                'main_thumb'
            ],
            Collection.objects.filter(
                id = 1
            ).values(
                'thumbnail_id__url'
            ).first()[
                'thumbnail_id__url'
            ]
        )

        self.assertTrue(
            res.json()[
                'range_list'
            ]
        )


    def test_paginate_req_contents_length(self):

        a, b, c = clnt.get(
            '/music/main'
        ).json()[
            'range_list'
        ][:3]

        self.assertEqual(
            len(
                clnt.get(
                    f'/music/main?collection_id={a}&collection_id={b}&collection_id={c}'
                ).json()[
                    'contents'
                ]
            ),
            3
        )

    def test_paginate_req_unexpected_keys(self):

        a, b, c = clnt.get(
            '/music/main'
        ).json()[
            'range_list'
        ][:3]

        res = clnt.get(
            f'/music/main?collection_id={a}&collection_id={b}&collction_id={c}'
        )

        def for_test():

            try:

                res.json()[
                    'main_thumb'
                ]

                res.json()[
                    'range_list'
                ]

                return True

            except KeyError:

                return False

        self.assertFalse(for_test())

