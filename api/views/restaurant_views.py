import json
from typing import Iterable
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.serializer import AddRestaurantSerializer, ImageSerializer, ServiceSerializer


@api_view(['POST'])
def addRestaurant(request):
    data = request.data
    restaurantDict = data.get('restaurant')
    if restaurantDict == None:
        return Response(data='No restaurant was provided', status=status.HTTP_400_BAD_REQUEST)
    if isinstance(restaurantDict, str):
        restaurantDict = json.loads(restaurantDict)
    restaurantDict['type'] = 'restaurant'
    amenities = data.get('amenities')
    if amenities == None:
        return Response(data='No amenities were provided', status=status.HTTP_400_BAD_REQUEST)
    if isinstance(amenities, str):
        amenities = json.loads(amenities)
        amenities = [int(i) for i in amenities]
    images = request.FILES
    restaurantSerializer = AddRestaurantSerializer(data=restaurantDict)
    if restaurantSerializer.is_valid():
        restaurant = restaurantSerializer.save()
        publicPlaceId = restaurant.id

        if isinstance(amenities, Iterable):
            for amenityId in amenities:
                serviceSerializer = ServiceSerializer(data={
                    'publicPlaceId': publicPlaceId,
                    'amenityId': amenityId,
                })
                if serviceSerializer.is_valid():
                    serviceSerializer.save()
                else:
                    return Response(serviceSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(images, Iterable):
            for imageKey in images.keys():
                imageSerializer = ImageSerializer(data={
                    'publicPlaceId': publicPlaceId,
                    'path': images[imageKey],
                })
                if imageSerializer.is_valid():
                    imageSerializer.save()
                else:
                    return Response(imageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(True, status=status.HTTP_201_CREATED)
    return Response(restaurantSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
