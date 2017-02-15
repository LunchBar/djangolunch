from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group

# class GroupMember(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     member = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='group',
#     )
#     is_leader = models.BooleanField(default=False)

    # count order !

class OrderForMenupic(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price = models.IntegerField()

class OrderGroup(Group):
    restaurant = models.OneToOneField('restaurants.Restaurant', on_delete=models.CASCADE)
    leader = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # TODO: delete behavior
