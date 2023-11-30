import json
from typing import Iterable
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
import rest_framework.filters as filters
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from api.serializer import AddHotelSerializer, AddRoomSerializer, AmenitySerializer, HotelResponseSerializer, HotelSerializer, ImageSerializer, AddHotelSerializer, PublicPlaceFullAddressSerializer, PublicPlaceSerializer, ServiceSerializer

from graduationapp.models import Amenities, Hotel, Images, PublicPlace, Service


@api_view(['GET'])
def hotels(request):
    return getHotels(request)
    # if request.method == 'GET':
    # return addHotel(request)


def getHotels(request):
    hotels = Hotel.objects.all()
    hotelsWithDetails = []
    for hotel in hotels:
        hotelsWithDetails.append(getHotelDetails(hotel, request))
    return Response(hotelsWithDetails, status=status.HTTP_200_OK)


def getHotelDetails(hotel, request):
    services = Service.objects.filter(publicPlaceId=hotel.id)
    hotelAmenities = []
    for service in services:
        hotelAmenities.append(service.amenityId)
    # hotelAmenities = Amenities.objects.filter(id__in=amenitiesIds)
    hotelImages = Images.objects.filter(publicPlaceId=hotel.id)

    return {
        'hotel': HotelResponseSerializer(hotel).data,
        'amenities': AmenitySerializer(hotelAmenities, many=True).data,
        'images': ImageSerializer(hotelImages, context={'request': request}, many=True).data,
        'location': PublicPlaceFullAddressSerializer(hotel).data
    }


# @api_view(['POST'])
# def addHotel(request):
#     data = request.data
#     print('Add Hotel Request Received')
#     print('Hotel Data Provided:' + getString(request.data))
#     hotelDict = data.get('hotel')
#     if hotelDict == None:
#         return Response(data='No hotel was provided', status=status.HTTP_400_BAD_REQUEST)
#     if isinstance(hotelDict, str):
#         hotelDict = json.loads(hotelDict)
#     hotelDict['type'] = 'hotel'
#     amenities = data.get('amenities')
#     if amenities == None:
#         return Response(data='No amenities were provided', status=status.HTTP_400_BAD_REQUEST)
#     if isinstance(amenities, str):
#         amenities = json.loads(amenities)
#         amenities = [int(i) for i in amenities]
#     images = request.FILES
#     hotelSerializer = AddHotelSerializer(data=hotelDict)
#     if hotelSerializer.is_valid():
#         hotel = hotelSerializer.save()
#         publicPlaceId = hotel.id

#         if isinstance(amenities, Iterable):
#             for amenityId in amenities:
#                 serviceSerializer = ServiceSerializer(data={
#                     'publicPlaceId': publicPlaceId,
#                     'amenityId': amenityId,
#                 })
#                 if serviceSerializer.is_valid():
#                     serviceSerializer.save()
#                 else:
#                     return Response(serviceSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         if isinstance(images, Iterable):
#             for imageKey in images.keys():
#                 imageSerializer = ImageSerializer(data={
#                     'publicPlaceId': publicPlaceId,
#                     'path': images[imageKey],
#                 })
#                 if imageSerializer.is_valid():
#                     imageSerializer.save()
#                 else:
#                     return Response(imageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         print('Add Hotel Request Was Handled Successfully')
#         return Response(True, status=status.HTTP_201_CREATED)
#     return Response(hotelSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelSearch(generics.ListAPIView):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
    filter_backends = [filters.OrderingFilter,
                       filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'numberOfStars']
    filterset_fields = ['streetId']
    search_fields = ['name']


@api_view(["POST"])
def addRoom(request):
    data = request.data
    roomSerializer = AddRoomSerializer(data=data)
    if roomSerializer.is_valid():
        roomSerializer.save()
        return Response(status=status.HTTP_201_CREATED, data=True)

    return Response(roomSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
