from django.urls import path

urlpatterns = [
    path(
        'music',
        include(
            'music.urls'
        )
    ),
]
