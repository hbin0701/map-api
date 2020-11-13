from rest_framework import serializers
from .models import Places, Reviews
from users.models import Users
from users.serializers import UserSerializer

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        depth = 1
        fields = ['latitude', 'longtitude', 'name', 'rating']


class RecommendedPlaceSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        # return in km.
        return round(float(obj.calc_distance) * 111111 / 1000, 2)

    class Meta:
        model = Places
        depth = 1
        fields = ['latitude', 'longtitude', 'name', 'rating', 'distance']


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    place = PlaceSerializer()

    class Meta:
        model = Reviews
        fields = ['id', 'author', 'place', 'comment', 'created_date', 'rating']

    def create(self, validated_data):
        # Place name might not be unique, so use place id.
        place = validated_data.pop('place')
        place_instance = Places.objects.get(id = place)
        # Author is always unique, as we prevented same username in registration.
        author = validated_data.pop('author')
        author_instance = Users.objects.get(username=author)
        instance = Reviews.objects.create(place=place_instance, author=author_instance, **validated_data)
        return instance 

     