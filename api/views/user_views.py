import json
from typing import Iterable
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
import rest_framework.filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from api.serializer import CuisineSerializer, ReservationRoomSerializer
from graduationapp.models import Cuisine, FarmBooking, RoomBooking, TableBooking


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
        'farms': ReservationRoomSerializer(farmBookings, many=True).data
    })
