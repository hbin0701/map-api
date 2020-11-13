import json
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views import View
from django.http import JsonResponse    
from .models import Places, Reviews
from users.models import Users
from .serializers import PlaceSerializer, ReviewSerializer, RecommendedPlaceSerializer
from django.db.models import Count, Avg, F, Func, Q

def get_nearby_places(request):
 if request.method == 'POST':
        # need to post latitude, longtitude, name, and size (optional)
        data = JSONParser().parse(request)
        try:
            size = data['size']
        except:
            # default
            size = "small"

        # Get places that are nearby in distance of 0.5, 1, 3 km accordingly.
        # assume 111 km = 1 degrees.
        if size = "small":
            distance = 0.5
        elif size = "middle":
            distance = 1
        elif size = "big":
            distance = 3

        distance = round(distance/111, 6)

        result = Places.objects.annotate(calc_distance=Func((F('latitude')- data['latitude'])** 2 + \
            (F('longtitude') - data['longtitude']) ** 2, function='SQRT')).filter(Q(~Q(calc_distance=0)\
                |~Q(name=data['name']))).filter(calc_distance__lt=distance).order_by('-rating')[:5]
        
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

def remove_reviews(request):
    # Delete my reviews
    if request.method == 'POST':
        data = JSONParser().parse(request)
        review = Reviews.objects.get(id=data['id'])
        review.delete()

        return JsonResponse({"message": "Review successfully removed."}, status=201)

def edit_reviews(request):     
    # Edit my reivews.
    if request.method == 'POST':
        review.rating = request.POST['rating']
        review.comment = request.POST['comment']
        review.save()
        return JsonResponse({"message": "Review succesfully edited."}, status=201)


def place_info(request):
    if request.method == 'POST':
        # need latitude , longtitude , place
        data = JSONParser().parse(request)

        target, created = Places.objects.get_or_create(
        latitude = data['latitude'],
        longtitude = data['longtitude'],
        defaults = {
            'name': data['place'],
            'rating': 0 
        })
        
        b = Places.objects.filter(latitude=data['latitude']).filter(longtitude=data['longtitude']).filter(name=data['place']).annotate(reviews_count = Count('reviewset')).annotate(temp_rating=Avg('reviewset__rating'))

        if created:
            target.rating = 0
        else:
            target.rating = list(b.values_list('temp_rating', flat=True))[0]

        target.save()
        nearby_places = get_nearby_places(request)    


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
