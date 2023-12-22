from django.urls import path

from api.v1.products.views import ProductListAPIView

urlpatterns = [
    path('', ProductListAPIView.as_view()),
]
