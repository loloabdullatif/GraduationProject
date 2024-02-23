import datetime
import json
from typing import Iterable
import pytz
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db.models import Q

import rest_framework.filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from api.serializer import AddRestaurantSerializer, AddRoomSerializer, AddTableSerializer, AmenitySerializer, ImageSerializer, RestaurantCuisineSerializer, RestaurantDetailsSerializer, ServiceSerializer, TableBookingSerializer, TableSerializer
from graduationProject import settings
from graduationapp.models import Images, Restaurant, Service, Table, TableBooking, TouristaUser


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
    cuisines = data.get('cuisines')
    if cuisines == None:
        return Response(data='No cuisines were provided', status=status.HTTP_400_BAD_REQUEST)
    if isinstance(cuisines, str):
        cuisines = json.loads(cuisines)
        cuisines = [int(i) for i in cuisines]
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

        if isinstance(cuisines, Iterable):
            for cuisineId in cuisines:
                restaurantCuisineSerializer = RestaurantCuisineSerializer(data={
                    'restaurantId': publicPlaceId,
                    'cuisineId': cuisineId,
                })
                if restaurantCuisineSerializer.is_valid():
                    restaurantCuisineSerializer.save()
                else:
                    return Response(restaurantCuisineSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


# TODO: Remove later
# @api_view(["POST"])
# def addRoom(request):
#     data = request.data
#     roomSerializer = AddRoomSerializer(data=data)
#     if roomSerializer.is_valid():
#         roomSerializer.save()
#         return Response(status=status.HTTP_201_CREATED, data=True)

#     return Response(roomSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Add table
@api_view(["POST"])
def addTable(request):
    data = request.data
    tableSerializer = AddTableSerializer(data=data)
    if tableSerializer.is_valid():
        tableSerializer.save()
        return Response(status=status.HTTP_201_CREATED, data=True)
    return Response(tableSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def allRestaurants(request):
    restaurants = Restaurant.objects.filter(isApproved=True)[:8]
    return Response(
        status=status.HTTP_200_OK,
        data=RestaurantDetailsSerializer(restaurants, many=True, context={
                                         "request": request},).data,
    )


@api_view(["GET"])
def restaurantTables(request):
    restaurantId = request.GET.get("restaurantId")
    if (restaurantId == None):
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
        )
    tables = Table.objects.filter(restaurantId=restaurantId)
    return Response(
        status=status.HTTP_200_OK,
        data=TableSerializer(tables, many=True).data,
    )


class RestaurantSearch(generics.ListAPIView):
    serializer_class = RestaurantDetailsSerializer
    queryset = Restaurant.objects.filter(isApproved=True)
    filter_backends = [filters.OrderingFilter,
                       filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['rating']
    filterset_fields = ['streetId']
    search_fields = ['name']


@api_view(['GET'])
def getAvailableTables(request, restaurantId):
    queryParams = request.GET
    try:
        capacity = int(queryParams.get('numberOfPeople'))
        checkInTime = datetime.datetime.strptime(
            queryParams.get('checkInTime'), '%Y-%m-%d %H:%M')
        checkoutTime = datetime.datetime.strptime(
            queryParams.get('checkoutTime'), '%Y-%m-%d %H:%M')
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Missing Query Args')

    restaurantTables = Table.objects.filter(
        restaurantId=restaurantId, capacity__gte=capacity)

    tableIds = [table.pk for table in restaurantTables]
    tableBookings = TableBooking.objects.filter(
        tableId__in=tableIds)
    excludedTables = []
    for booking in tableBookings:
        if (excludedTables.__contains__(booking.tableId)):
            continue
        if (checkBookingOverlappingAgainstRange(booking=booking, checkInTime=checkInTime, checkoutTime=checkoutTime)):
            excludedTables.append(booking.tableId)

    availableTables = Table.objects.filter(restaurantId=restaurantId).exclude(
        Q(pk__in=[table.pk for table in excludedTables]) | Q(capacity__lt=capacity))
    return Response(status=status.HTTP_200_OK, data=TableSerializer(availableTables, many=True).data)


def checkTableAvailability(table, checkInTime, checkoutTime):
    tableBookings = TableBooking.objects.filter(tableId=table.id)
    if (checkBookingListOverlappingAgainstRange(bookings=tableBookings, checkInTime=checkInTime, checkoutTime=checkoutTime)):
        return False
    return True


def checkBookingListOverlappingAgainstRange(bookings, checkInTime, checkoutTime):
    for booking in bookings:
        if (checkBookingOverlappingAgainstRange(booking=booking, checkInTime=checkInTime, checkoutTime=checkoutTime)):
            return True
    return False


def checkBookingOverlappingAgainstRange(booking, checkInTime, checkoutTime):
    settings_time_zone = pytz.timezone(settings.TIME_ZONE)
    checkInTime = checkInTime.astimezone(settings_time_zone)
    checkoutTime = checkoutTime.astimezone(settings_time_zone)
    if (checkInTime <= booking.checkInTime) and (checkoutTime >= booking.checkoutTime):
        return True
    if (checkInTime >= booking.checkInTime) and (checkoutTime <= booking.checkoutTime):
        return True
    if (checkoutTime >= booking.checkInTime) and (checkInTime <= booking.checkoutTime):
        return True
    if checkInTime <= booking.checkoutTime and checkoutTime >= booking.checkoutTime:
        return True
    return False


@api_view(['POST'])
def bookTable(request):
    data = request.data
    try:
        userId = data.get('userId')
        tableId = data.get('tableId')
        if (userId == None) or (tableId == None):
            raise ValueError()
        checkInTime = datetime.datetime.strptime(
            data.get('checkInTime'), '%Y-%m-%d %H:%M')
        checkoutTime = datetime.datetime.strptime(
            data.get('checkoutTime'), '%Y-%m-%d %H:%M')
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Missing Body Args')

    try:
        table = Table.objects.get(id=tableId)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='Table does not exist')
    try:
        user = TouristaUser.objects.get(id=userId)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='User does not exist')
    if (checkTableAvailability(table=table, checkInTime=checkInTime, checkoutTime=checkoutTime) == False):
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='Table has been reserved by someone else, try another table')

    tableBookingSerializer = TableBookingSerializer(data=data)
    if tableBookingSerializer.is_valid():
        tableBookingSerializer.save()
        return Response(status=status.HTTP_201_CREATED, data='Booking Successful')

    return Response(tableBookingSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
