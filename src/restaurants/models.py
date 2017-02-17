from django.conf import settings
from django.db import models

class Restaurant(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # TODO: test everyone can delete the restaurant if owner has been deleted.
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_restaurants'
    )
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50, blank=True, default='')
    # a restaurant has a menu_picture or MenuItem records.
    menu_picture = models.URLField(max_length=50, blank=True)
    note = models.TextField(blank=True, default='')
    is_ok = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MenuItem(models.Model):

    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
        null=True,
        related_name='menu_items'
    )
    name = models.CharField(max_length=20)
    price = models.IntegerField()

    def __str__(self):
        return self.name
