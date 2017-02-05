from django.db import models

class NextweekRestaurant(models.Model):
    ''' id=1 means Monday ... etc. '''
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.CASCADE, # TODO: Umm...
        related_name='nextweek'
    )
