import jwt

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from YoutubeMuzic.settings import (
    SECRET_KEY,
    ALGORITHM
)
from .models import User


def login_required(func):
    def login_wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization']
            user_id = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)['id']
            user = get_object_or_404(User, id=user_id)
            return func(self, request, user)

        except KeyError:
            return HttpResponse(status=400)
        except jwt.exceptions.DecodeError:
            return HttpResponse(status=400)
    return login_wrapper
