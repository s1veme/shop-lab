from django.urls import path

from api.common.health.views import HealthView

urlpatterns = [
    path('', HealthView.as_view()),
]
