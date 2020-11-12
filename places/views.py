import json
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views import View
from django.http import JsonResponse    
from .models import Places, Reviews
from .serializers import PlaceSerializer, ReviewSerializer


def get_my_reviews(request):
    # Get all reviews.
    pass

def process_rating(request):
    # Get the review for the place.
    pass

def process_reviews(request, x=0, y=0):
    if request.method == 'GET': 
        place_id = list(Places.objects.filter(longtitude=x).filter(latitude=y).values("id"))[0]['id']
        reviewset = Reviews.objects.filter(place_id=place_id)
        serializer = ReviewSerializer(reviewset, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        # NEED TO POST:
        # author, place, latitude. longtitude, comment, rating
        data = JSONParser().parse(request)

        # If place doesn't exist, register the place first.
        a, created = Places.objects.get_or_create(
            latitude = data['latitude'],
            longtitude = data['longtitude'],
            defaults = {
                'name': data['place'],
                'rating': 0 
            }
        )

        # Get the ids.
        place_id = a.id
        author_id = list(Users.objects.filter(username=data['author']).values_list('id', flat=True))[0]

        a = Reviews(
            "author_id": author_id,
            "place_id": place_id,
            "comment": data['comment'],
            "rating": data['rating']
        ).save()
    
        return JsonResponse({"message": "Review succesfully saved."}, status=201)
