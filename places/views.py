import json
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views import View
from django.http import JsonResponse, HttpResponse 
from .models import Places, Reviews
from users.models import Users
from .serializers import PlaceSerializer, ReviewSerializer, RecommendedPlaceSerializer, PlaceInfoSerializer
from django.db.models import Count, Avg, F, Func, Q
from django.utils.safestring import mark_safe

def get_nearby_places(request):
    '''
    returns 5 nearby_places with higest rating.
    '''
    if request.method == 'POST':
        # need to post latitude, longtitude, place, and size (optional)
        data = JSONParser().parse(request)

        # If place doesn't exist, register it first·
        a, created = Places.objects.get_or_create(
            latitude = data['latitude'],
            longtitude = data['longtitude'],
            defaults = {
                'name': data['place'],
                'rating': 0 
            }
        )

        try:
            size = data['size']
        except:
            # default
            size = "small"

        # Get places that are nearby in distance of 0.5, 1, 3 km accordingly.
        # assume 111 km = 1 degrees.
        if size == "small":
            distance = 0.5
        elif size == "middle":
            distance = 1
        elif size == "big":
            distance = 3

        distance = round(distance/111, 6)

        result = Places.objects.annotate(calc_distance=Func((F('latitude')- data['latitude'])** 2 + \
            (F('longtitude') - data['longtitude']) ** 2, function='SQRT')).filter(Q(~Q(calc_distance=0)\
                |~Q(name=data['place']))).filter(calc_distance__lt=distance).order_by('-rating')[:5]
        
        serializer = RecommendedPlaceSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)

def get_my_reviews(request):
    # Get all reviews, just send the "username" to get all username's reviews.
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = list(Users.objects.filter(username=data['username']).values_list("id", flat=True))[0]
        reviewset = Reviews.objects.filter(author_id = user_id)
        serializer = ReviewSerializer(reviewset, many=True)
        return JsonResponse(serializer.data, safe=False)


'''
remove_reviews and edit_reviews will be only accessible through my_reviews page
where each review will be returned with its unique id.
'''

def remove_reviews(request):
    # Delete my reviews
    # Need id of the review.
    if request.method == 'POST':
        data = JSONParser().parse(request)
        review = Reviews.objects.get(id=data['id'])
        review.delete()

        return JsonResponse({"message": "Review successfully removed."}, status=201)

def edit_reviews(request):     
    # Edit my reivews.
    # Need id of the review, new_rating, new_comment
    if request.method == 'POST':
        data = JSONParser().parse(request)
        review = Reviews.objects.get(id=data['id'])
        review.rating = data['rating']
        review.comment = data['comment']
        review.save()
        return JsonResponse({"message": "Review succesfully edited."}, status=201)

def place_info(request):
    if request.method == 'POST':
        # needs latitude , longtitude , place
        # Returns all the infos for place, like:
        # latitude, longtitude, name, reviews_count, rating, and the most recent three reviews.
        data = JSONParser().parse(request)

        target, created = Places.objects.get_or_create(
        latitude = data['latitude'],
        longtitude = data['longtitude'],
        defaults = {
            'name': data['place'],
            'rating': 0 
        })
        
        temp = Places.objects.filter(latitude=data['latitude']).filter(longtitude=data['longtitude']).filter(name=data['place'])\
            .annotate(reviews_count = Count('reviewset')).annotate(temp_rating=Avg('reviewset__rating'))
        
        num = list(temp.values_list('temp_rating', flat=True))[0]
        
        if num != None:
            target.rating = list(temp.values_list('temp_rating', flat=True))[0]
            target.save()

        serializer = PlaceInfoSerializer(temp, many=True)
        place_id = list(Places.objects.filter(latitude=data['latitude']).filter(longtitude=data['longtitude']).filter(name=data['place'])\
            .values_list("id", flat=True))[0]

        reviewset = Reviews.objects.filter(place_id=place_id).order_by('-created_date')[:3]
        reviewset = ReviewSerializer(reviewset, many=True)

        context = {
            'place_info': serializer.data,
            'reviews': reviewset.data
        }

        data = mark_safe(json.dumps(context, indent=4, sort_keys=True, default=str))
        return HttpResponse(data, content_type='application/json')

def process_reviews(request, x=0, y=0):
    # Gets all the Reviews for a place. This is for when user clicked "More Reviews."
    if request.method == 'GET': 
        place_id = list(Places.objects.filter(longtitude=x).filter(latitude=y).values("id"))[0]['id']
        reviewset = Reviews.objects.filter(place_id=place_id)
        serializer = ReviewSerializer(reviewset, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        # NEED TO POST:
        # username, place, latitude. longtitude, comment, rating
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
        author_id = list(Users.objects.filter(username=data['username']).values_list('id', flat=True))[0]

        a = Reviews(
            author_id =  author_id, 
            place_id= place_id,
            comment= data['comment'],
            rating= data['rating']
        ).save()
    
        return JsonResponse({"message": "Review succesfully saved."}, status=201)
