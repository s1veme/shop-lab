from django.db import models


class Product(models.Model):
    title = models.TextField()
    description = models.TextField()
    price = models.BigIntegerField()
    image = models.ImageField(upload_to='products')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
