from django.db import models
from django.contrib.auth.models import AbstractUser

# extend default User model.
class User(AbstractUser):
    deposit = models.IntegerField(default=0)
    # any order will transfer to MenuItem first.
    order = models.ForeignKey(
        'restaurants.MenuItem',
        on_delete=models.CASCADE, # TODO: Umm...
        null=True,
        # related_name='order'
    )
    order_note = models.TextField(blank=True, default='')
