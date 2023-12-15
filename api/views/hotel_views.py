from datetime import datetime
import json
from typing import Iterable
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
import rest_framework.filters as filters
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from api.serializer import AddHotelSerializer, AddRoomSerializer, AmenitySerializer, HotelDetailsSerializer, HotelResponseSerializer, PublicPlaceDetailsSerializer, ImageSerializer, AddHotelSerializer, PublicPlaceFullAddressSerializer, PublicPlaceSerializer, ReservationRoomSerializer, ServiceSerializer
from django.db.models import Q
from graduationapp.models import Amenities, Hotel, Images, PublicPlace, Room, RoomBooking, Service


@api_view(['GET'])
def hotels(request):
    return getHotels(request)
    # if request.method == 'GET':
    # return addHotel(request)


def getHotels(request):
    hotels = Hotel.objects.all()
    return Response(HotelDetailsSerializer(hotels, context={'request': request}, many=True).data, status=status.HTTP_200_OK)


def getString(param):
    return str(param)


class AddHotelAPIView(APIView):
    def post(self, request):
        requestData = request.data
        newData = {
            'hotel': json.loads(requestData['hotel']),
            'amenities': json.loads(requestData['amenities']),
            'images': list(request.FILES.values()),
        }
        serializer = AddHotelSerializer(data=newData)
        if serializer.is_valid():
            serializer.save()
            return Response(True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelSearch(generics.ListAPIView):
    serializer_class = HotelDetailsSerializer
    queryset = Hotel.objects.all()
    filter_backends = [filters.OrderingFilter,
                       filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'numberOfStars']
    filterset_fields = ['streetId']
    search_fields = ['name']


@api_view(['GET'])
def getAvailableRooms(request, hotelId):
    queryParams = request.GET
    try:
        numberOfPeople = int(queryParams.get('numberOfPeople'))
        checkInDate = datetime.strptime(
            queryParams.get('checkInDate'), '%Y-%m-%d').date()
        checkOutDate = datetime.strptime(
            queryParams.get('checkOutDate'),  '%Y-%m-%d').date()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Missing Query Args')

    hotelRooms = Room.objects.filter(
        hotelId=hotelId, numberOfPeople__gte=numberOfPeople)

    hotelRoomIds = [room.pk for room in hotelRooms]
    hotelBookings = RoomBooking.objects.filter(
        roomId__in=hotelRoomIds)
    excludedRooms = []
    for booking in hotelBookings:
        if (excludedRooms.__contains__(booking.roomId)):
            continue
        if (checkInDate <= booking.checkInDate) and (checkOutDate >= booking.checkoutDate):
            excludedRooms.append(booking.roomId)
            print('excluded on outer')
            continue
        if (checkInDate >= booking.checkInDate) and (checkOutDate <= booking.checkoutDate):
            excludedRooms.append(booking.roomId)
            print('excluded on inner')
            continue
        if (checkOutDate >= booking.checkInDate) and (checkInDate <= booking.checkoutDate):
            excludedRooms.append(booking.roomId)
            print('excluded on 1')
            continue
        if checkInDate <= booking.checkoutDate and checkOutDate >= booking.checkoutDate:
            print('excluded on 2')
            excludedRooms.append(booking.roomId)
            continue
    numberOfNights = (checkOutDate - checkInDate).days + 1
    availableRooms = Room.objects.exclude(
        Q(pk__in=[room.pk for room in excludedRooms]) | Q(numberOfPeople__lt=numberOfPeople))
    return Response(status=status.HTTP_200_OK, data=ReservationRoomSerializer(availableRooms, context={'numberOfNights': numberOfNights}, many=True).data)
