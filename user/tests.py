import json

from django.test import TestCase, Client

from user.models import User
from YoutubeMuzic.settings import (
    right_id,
    wrong_id,
    right_token,
    jwt_token,
)


class SignInViewTest(TestCase):
    maxDiff = None

    def setUp(self):
        User(
            google_id='2314324'
        ).save()

    def tearDown(self):
        User.objects.get(google_id='2314324').delete()

    def test_sign_in_success(self):
        client = Client()
        data = {"id": right_id, "token": right_token}
        response = client.post('/user/signin', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['token'], jwt_token)

    def test_sign_in_wrong_id_token(self):
        client = Client()
        data = {"id": wrong_id, "token": right_token}
        response = client.post('/user/signin', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_sign_in_with_wrong_key(self):
        client = Client()
        data = {"if": wrong_id, "tooken": right_token}
        response = client.post('/user/signin', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

class RecentViewTest(TestCase):
    def setUp(self):
        User(
            google_id='2314324'
        ).save()

    def tearDown(self):
        User.objects.get(google_id='2314324').delete()

    def test_post_recent_media_success(self):
        client = Client()
        data = {
            "media_id": 2
        }
        header = {'HTTP_authorization': jwt_token}
        response = client.post('/user/recent/media', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)

    def test_post_recent_playlist_success(self):
        client = Client()
        data = {
            "playlist_id": 2
        }
        header = {'HTTP_authorization': jwt_token}
        response = client.post('/user/recent/playlist', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)

    def test_post_recent_media_login_failure(self):
        client = Client()
        data = {
            "media_id": 2
        }
        header = {'HTTP_authorization': 'dfgdsfg'}
        response = client.post('/user/recent/media', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_playlist_login_failure(self):
        client = Client()
        data = {
            "media_id": 5
        }
        header = {'HTTP_authorization': 'sdfgdfgs'}
        response = client.post('/user/recent/playlist', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_media_key_error(self):
        client = Client()
        data = {
            "media": 2
        }
        header = {'HTTP_authorization': jwt_token}
        response = client.post('/user/recent/media', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_playlist_key_error(self):
        client = Client()
        data = {
            "list_id": 2
        }
        header = {'HTTP_authorization': jwt_token}
        response = client.post('/user/recent/playlist', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_media_value_error(self):
        client = Client()
        data = {
            "media": 'dsfsd'
        }
        header = {'HTTP_authorization': jwt_token}
        response = client.post('/user/recent/media', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_playlist_value_error(self):
        client = Client()
        data = {
            "media": '43534'
        }
        header = {'HTTP_authorization': jwt_token}
        response = client.post('/user/recent/playlist', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_media_does_not_exist(self):
        client = Client()
        data = {
            "media_id": 1275417598
        }
        header = {'HTTP_authorization': jwt_token}
        response = client.post('/user/recent/media', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 404)

    def test_post_recent_playlist_does_not_exist(self):
        client = Client()
        data = {
            "playlist_id": 59432708942
        }
        header = {'HTTP_authorization': jwt_token}
        response = client.post('/user/recent/playlist', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 404)