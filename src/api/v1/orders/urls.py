from django.urls import path

from api.v1.orders.views import OrderCreateAPIView

urlpatterns = [
    path('', OrderCreateAPIView.as_view()),
]
