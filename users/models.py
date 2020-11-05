from django.db import models
from django.utils import timezone

# class Place(models.Model):
#     # latitude = models.FloatField(max_digits = 12, deicmal_places= 6)
#     # longtitude = models.FloatField(max_digits = 12, deicmal_places= 6)
#     name = models.CharField(max_length = 20)
    
#     # These two need to be connected? I guess.

#     # rating = models.FloatField(max_digits = 3, decimal_places=2)
#     # comment =

class Users(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    email = models.CharField(max_length = 100)

    class Meta:
        db_table = "Users"
        
class Reviews(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='reveiwset')
    commgitent = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
