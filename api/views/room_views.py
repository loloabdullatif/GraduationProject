from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializer import AddRoomSerializer, RoomSerializer

from graduationapp.models import Room



@api_view(["GET"])
def hotelRooms(request):
    hotelId=request.GET.get("hotelId")
    if(hotelId==None):
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
