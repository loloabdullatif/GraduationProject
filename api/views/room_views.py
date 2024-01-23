from collections import ChainMap
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializer import AddRoomBookingSerializer, AddRoomSerializer, AvailableReservationRoomSerializer, RoomSerializer
from django.db.models import Q
from datetime import datetime

from graduationapp.models import Room, RoomBooking, TouristaUser


@api_view(["GET"])
def hotelRooms(request):
    hotelId = request.GET.get("hotelId")
    if (hotelId == None):
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
        )
    rooms = Room.objects.filter(hotelId=hotelId)
    return Response(
        status=status.HTTP_200_OK,
        data=RoomSerializer(rooms, many=True).data,
    )


@api_view(["POST"])
def addRoom(request):
    data = request.data
    roomSerializer = AddRoomSerializer(data=data)
    if roomSerializer.is_valid():
        roomSerializer.save()
        return Response(status=status.HTTP_201_CREATED, data=True)

    return Response(roomSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getAvailableRooms(request, hotelId):
    queryParams = request.GET
    try:
        numberOfPeople = int(queryParams.get('numberOfPeople'))
        checkInDate = datetime.strptime(
            queryParams.get('checkInDate'), '%Y-%m-%d').date()
        checkoutDate = datetime.strptime(
            queryParams.get('checkoutDate'),  '%Y-%m-%d').date()
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
        if (checkBookingOverlappingAgainstRange(booking=booking, checkInDate=checkInDate, checkoutDate=checkoutDate)):
            excludedRooms.append(booking.roomId)

    numberOfNights = (checkoutDate - checkInDate).days + 1
    availableRooms = Room.objects.filter(hotelId=hotelId).exclude(
        Q(pk__in=[room.pk for room in excludedRooms]) | Q(numberOfPeople__lt=numberOfPeople))
    return Response(status=status.HTTP_200_OK, data=AvailableReservationRoomSerializer(availableRooms, context={'numberOfNights': numberOfNights}, many=True).data)


def checkRoomAvailability(room, checkInDate, checkoutDate):
    roomBookings = RoomBooking.objects.filter(roomId=room.id)
    if (checkBookingListOverlappingAgainstRange(bookings=roomBookings, checkInDate=checkInDate, checkoutDate=checkoutDate)):
        return False
    return True


def checkBookingListOverlappingAgainstRange(bookings, checkInDate, checkoutDate):
    for booking in bookings:
        if (checkBookingOverlappingAgainstRange(booking=booking, checkInDate=checkInDate, checkoutDate=checkoutDate)):
            return True
    return False


def checkBookingOverlappingAgainstRange(booking, checkInDate, checkoutDate):
    if (checkInDate <= booking.checkInDate) and (checkoutDate >= booking.checkoutDate):
        print('excluded on outer')
        return True
    if (checkInDate >= booking.checkInDate) and (checkoutDate <= booking.checkoutDate):
        print('excluded on inner')
        return True
    if (checkoutDate >= booking.checkInDate) and (checkInDate <= booking.checkoutDate):
        print('excluded on 1')
        return True
    if checkInDate <= booking.checkoutDate and checkoutDate >= booking.checkoutDate:
        print('excluded on 2')
        return True
    return False


@api_view(['POST'])
def bookRoom(request):
    data = request.data
    try:
        userId = data.get('userId')
        roomId = data.get('roomId')
        if (userId == None) or (roomId == None):
            raise ValueError()
        checkInDate = datetime.strptime(
            data.get('checkInDate'), '%Y-%m-%d').date()
        checkoutDate = datetime.strptime(
            data.get('checkoutDate'),  '%Y-%m-%d').date()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Missing Body Args')

    try:
        room = Room.objects.get(id=roomId)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='Room does not exist')
    try:
        user = TouristaUser.objects.get(id=userId)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='User does not exist')
    if (checkRoomAvailability(room=room, checkInDate=checkInDate, checkoutDate=checkoutDate) == False):
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='Room has been reserved by someone else, try another room')

    price = int(((checkoutDate-checkInDate).days + 1)*room.price)
    bookingDetails = dict(ChainMap({"price": price}, data))
    roomBookingSerializer = AddRoomBookingSerializer(data=bookingDetails)
    if roomBookingSerializer.is_valid():
        roomBookingSerializer.save()
        return Response(status=status.HTTP_201_CREATED, data='Booking Successful')

    return Response(roomBookingSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def deleteBooking(request, bookingId):
    try:
        booking = RoomBooking.objects.get(id=bookingId)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except RoomBooking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)