from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='group_member',
    )
    is_leader = models.BooleanField(default=False)
    # any order will transfer to MenuItem first.
    item = models.ForeignKey(
        'restaurants.MenuItem',
        on_delete=models.CASCADE, # TODO: Umm...
        # related_name='order'
    )
    # count = models.IntegerField(default=1)
    note = models.TextField(blank=True, default='')
