from django.urls import path, include

from .views import (
    StreamView,
    MainView,
    ListView,
)

urlpatterns = [
    path('/<int:media_id>',StreamView.as_view()),
    path('/main',MainView.as_view()),
    path('/list/<int:list_id>',ListView.as_view()),
]
