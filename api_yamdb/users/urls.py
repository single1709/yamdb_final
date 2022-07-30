from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import RegisterUser, TokenCheck, UsersViewSet

app_name = 'users'

router_v1 = SimpleRouter()
router_v1.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/', include([
        path('signup/', RegisterUser.as_view(), name='register_user'),
        path('token/', TokenCheck.as_view(), name='take_token'),
    ])),
    path('', include(router_v1.urls)),
]
