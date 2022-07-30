from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/', include('api.urls', namespace='api')),
]
