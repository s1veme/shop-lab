from django.urls import path

from api.v1.users.views import UserCreateAPIView

urlpatterns = [
    path('', UserCreateAPIView.as_view()),
]
