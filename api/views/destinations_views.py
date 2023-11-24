import json
from typing import Iterable
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
import rest_framework.filters as filters
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from api.serializer import AddHotelSerializer, AddRoomSerializer, AmenitySerializer, HotelResponseSerializer, ImageSerializer, AddHotelSerializer, PublicPlaceSerializer, ServiceSerializer, TouristDestinationBaseSerializer, TouristDestinationDisplaySerializer

from graduationapp.models import Amenities, Hotel, Images, PublicPlace, Service, TouristDestination


@api_view(['GET'])
def getDestinations(request):

    destinations = TouristDestination.objects.all()
    serializer = TouristDestinationDisplaySerializer(
        destinations, many=True, context={'request': request})
    return Response(serializer.data)
