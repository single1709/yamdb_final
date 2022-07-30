from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('v1/', include('users.urls', namespace='users')),
    path('v1/', include('titles.urls', namespace='titles')),
    path('v1/', include('reviews.urls', namespace='reviews')),
]
