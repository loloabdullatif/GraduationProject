import json
from typing import Iterable
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
import rest_framework.filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from api.serializer import CuisineSerializer, FarmReservationSerializer, PublicPlaceSerializer, ReservationRoomSerializer, UserFavoritePropertySerializer
from graduationapp.models import Cuisine, FarmBooking, PublicPlace, RoomBooking, TableBooking


@api_view(["GET"])
def getMyReservations(request):
    userId = request.GET.get('userId')
    if (userId is None):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    roomBookings = RoomBooking.objects.filter(userId=userId)
    farmBookings = FarmBooking.objects.filter(userId=userId)
    tableBookings = TableBooking.objects.filter(userId=userId)
    return Response({
        'hotels': ReservationRoomSerializer(roomBookings, many=True).data,
        'farms': FarmReservationSerializer(farmBookings, many=True).data
    })


@api_view(["GET"])
def getMyFavorites(request):
    propertyIds = request.GET.get('propertyIds')
    try:
        propertyIds = list(json.loads(propertyIds))
        if not isinstance(propertyIds, list):
            raise ValueError()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Invalid or No ids were provided')

    properties = PublicPlace.objects.filter(id__in=propertyIds)
    return Response(UserFavoritePropertySerializer(properties, many=True, context={'request': request},).data)
