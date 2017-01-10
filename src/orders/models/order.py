from django.conf import settings
from django.db import models

# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='order'
    )
    # any order will transfer to MenuItem first.
    item = models.ForeignKey(
        'restaurants.MenuItem',
        on_delete=models.CASCADE, # TODO: Umm...
        related_name='order'
    )
    # count = models.IntegerField(default=1)
    note = models.TextField(blank=True, default='')

    def __str__(self):
        return '{customer} order {item} x{count}'.format(
            customer=self.customer, item_name=self.item, count=self.count
        )
