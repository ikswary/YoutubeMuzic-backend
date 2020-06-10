from django.urls import path

from .views import (
    GoogleSignInView,
    RecentMediaView,
    RecentPlaylistView,
    EvaluationView
)

urlpatterns = [
    path('/signin'          , GoogleSignInView.as_view())   , 
    path('/recent/media'    , RecentMediaView.as_view())    , 
    path('/recent/playlist' , RecentPlaylistView.as_view()) , 
    path('/like'            , EvaluationView.as_view()),
    path(''                 , UserView.as_view())
]
