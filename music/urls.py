from django.urls import path
from .views import StreamView

urlpatterns = [
   path('/<int:media_id>', StreamView.as_view()),
]
