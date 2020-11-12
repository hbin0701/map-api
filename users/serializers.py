from django.forms import widgets
from rest_framework import serializers
from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Users
        fields = ['id', 'username', 'password', 'email']