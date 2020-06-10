from django.urls import path, include

from .views import (
    StreamView,
    MainView,
    ListView,
    HotListView,
)

urlpatterns = [
    path('/<int:media_id>',StreamView.as_view()),
    path('/main',MainView.as_view()), # page 에 맞추면 안됨
    path('/list/<int:list_id>',ListView.as_view()),
    path('/hot',HotListView.as_view()),
]
