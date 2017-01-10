from django.db import models
from django.contrib.auth.models import AbstractUser

# extend default User model.
class User(AbstractUser):
    deposit = models.IntegerField(default=0)
