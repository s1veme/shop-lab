from rest_framework.generics import ListAPIView

from apps.products.models import Product
from api.v1.products.serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
