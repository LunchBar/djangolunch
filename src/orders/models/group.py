from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group

class ExtendGroup(models.Model):
    group = models.OneToOneField(Group)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # TODO: random choose another as leader?
        on_delete=models.SET_NULL,
        null=True,
        related_name='lead_group'
    )
    # member ?l

# class Membership(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
