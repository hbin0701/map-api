from django.db import models
from django.utils import timezone
from users.models import Users

class Places(models.Model):
    latitude = models.DecimalField(max_digits = 12, decimal_places= 6)
    longtitude = models.DecimalField(max_digits = 12, decimal_places= 6)
    name = models.CharField(max_length = 20)
    rating = models.DecimalField(max_digits = 3, decimal_places = 2)
    
    class Meta:
        db_table = "Places"

# Create your models here.
class Reviews(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='reviewset')
    place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name = 'reviewset')
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    
    class Meta:
        db_table = "Reviews"
