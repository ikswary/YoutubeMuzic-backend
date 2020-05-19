from django.urls import path

from .views import GoogleSignInView

urlpatterns = [
    path('/signin', GoogleSignInView.as_view())
]
