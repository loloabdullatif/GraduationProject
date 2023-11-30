from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializer import RoomSerializer

from graduationapp.models import Room



@api_view(["GET"])
def allRooms(request):
    rooms = Room.objects.all()
    return Response(
        status=status.HTTP_200_OK,
        data=RoomSerializer(rooms, many=True).data,
    )
    

# @api_view(['GET'])
# def allRooms(request):
#     id = request.GET.get('id')
#     if id != None:
#         return getRoomById(id)
#     roomid = request.GET.get('roomid')
#     if roomid != None:
#         return getCitiesInGovernorate(roomid)
#     rooms = Room.objects.all()
#     return Response(RoomSerializer(rooms, many=True).data)


# def getRoomById(id):
#     try:
#         room = Room.objects.get(id=id)
#     except Room.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     return Response(RoomSerializer(room, many=False).data)
