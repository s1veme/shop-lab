from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=CurrentUserDefault(),
    )

    class Meta:
        model = Order
        fields = [
            'full_name',
            'address',
            'email',
            'user',
            'product',
        ]
