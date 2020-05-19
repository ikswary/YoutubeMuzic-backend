from django.urls import path, include

urlpatterns = [
<<<<<<< HEAD
    path('music',include('music.urls')),
]
=======
    path('music', include('music.urls')),
    path('user', include('user.urls'))
]
>>>>>>> 57f6e040a085ef0efd8894e415d05267af48742e
