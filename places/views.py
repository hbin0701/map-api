import json
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views import View
from django.http import JsonResponse    
from .models import Places, Reviews
from .serializers import PlaceSerializer, ReviewSerializer

def process_reviews(request, x=0, y=0):
    if request.method == 'GET':
        place_id = list(Places.objects.filter(longtitude=x).filter(latitude=y).values("id"))[0]['id']
        reviewset = Reviews.objects.filter(place_id=place_id)
        serializer = ReviewSerializer(reviewset, many=True)
        print("serializer", serializer)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        # NEED TO POST:
        # username, name, latitude. longtitude, comment, rating

        data = JSONParser().parse(request)
        target = Places.objects.filter(latitude = data['latitude']).filter(longtitude = data['longtitude'])
        if target.exists(): 
            serializer = ReviewSerializer(data=data)
            if serializer.is_valid():   
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        else:
            # Place doesn't exist.
            pass
