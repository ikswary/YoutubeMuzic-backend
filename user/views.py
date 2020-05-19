import json
import requests
import jwt

from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import User
from YoutubeMuzic.settings import SECRET_KEY


class GoogleSignInView(View):
    GOOGLE_AUTH_URL = 'https://oauth2.googleapis.com/tokeninfo?id_token='
    CORRECT_ISS_LIST = ['accounts.google.com', 'https://accounts.google.com']

    def post(self, request):
        try:
            data = json.loads(request.body)
            google_id = data['id']
            token = data['token']

            token_data = json.loads(requests.get(self.GOOGLE_AUTH_URL + token).text)

            if (token_data['iss'] not in self.CORRECT_ISS_LIST) or (
                    token_data['sub'] != google_id):
                return JsonResponse({'message': 'MODIFIED_TOKEN'}, status=401)

            user = User.objects.get_or_create(google_id=google_id)
            token = jwt.encode(
                {'id': user[0].id}, SECRET_KEY, 'HS256'
            ).decode('utf-8')

            return JsonResponse({'token': token}, status=200)

        except KeyError:
            return HttpResponse(status=400)
