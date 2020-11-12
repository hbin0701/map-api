from rest_framework import serializers
from .models import Places, Reviews
from users.models import Users
from users.serializers import UserSerializer

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        depth = 1
        fields = ['latitude', 'longtitude', 'name', 'rating']

class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    place = PlaceSerializer()

    class Meta:
        model = Reviews
        fields = ['author', 'place', 'comment', 'created_date', 'rating']

    def create(self, validated_data):
        place = validated_data.pop('place')
        place_instance = Places.objects.get(name=place)
        author = validated_data.pop('author')
        author_instance = Users.objects.get(username=author)
        instance = Reviews.objects.create(place=place_instance, author=author_instance, **validated_data)
        return instance   