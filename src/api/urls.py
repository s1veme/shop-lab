from django.urls import include, path

urlpatterns = [
    path('common/', include('api.common.urls')),
    path('v1/', include('api.v1.urls')),
]
