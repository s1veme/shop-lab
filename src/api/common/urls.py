from django.urls import include, path


urlpatterns = [
    path('health', include('api.common.health.urls')),
    path('auth', include('api.common.auth.urls')),
]
