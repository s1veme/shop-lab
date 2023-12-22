from django.db import models

from apps.products.models import Product
from apps.users.models import User


class Order(models.Model):
    full_name = models.TextField()
    address = models.TextField()
    email = models.EmailField()

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.full_name} | {self.address} | {self.email}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
