import json

from django.test import TestCase, Client

from YoutubeMuzic.settings import (
    right_id,
    wrong_id,
    right_token,
    jwt_token,
)


class SignInViewTest(TestCase):
    maxDiff = None

    def test_sign_in_success(self):
        client = Client()
        data = {"id": self.right_id, "token": self.right_token}
        response = client.post('/user/signin', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['token'], self.jwt_token)

    def test_sign_in_wrong_id_token(self):
        client = Client()
        data = {"id": self.wrong_id, "token": self.right_token}
        response = client.post('/user/signin', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_sign_in_with_wrong_key(self):
        client = Client()
        data = {"if": self.wrong_id, "tooken": self.right_token}
        response = client.post('/user/signin', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
