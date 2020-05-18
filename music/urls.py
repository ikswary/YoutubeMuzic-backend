from django.urls import path, include

from .views import (
    StreamView,
    MainView
)

urlpatterns = [
    path(
        '/<int:media_id>',
        StreamView.as_view()
    ),
    path(
        '/main',
        MainView.as_view()
    ),
]
