from django.db import models
from django.utils import timezone

class Users(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    email = models.CharField(max_length = 100)

    class Meta:
        db_table = "Users"


