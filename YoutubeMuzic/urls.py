from django.urls import path, include

urlpatterns = [
    path('music',include('music.urls')),
]
