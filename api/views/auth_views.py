from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.response import Response
from api.serializer import AddUserSerializer, UpdateDataSerializer, UserReturnSerializer
from graduationapp.models import TouristaUser


@api_view(['POST'])
def login(request):
    userName = request.data.get('userName')
    password = request.data.get('password')
    try:
        user = TouristaUser.objects.get(userName=userName, password=password)
    except TouristaUser.DoesNotExist:
        return Response(False)
    return Response(UserReturnSerializer(user).data)


@api_view(['GET'])
def getById(request):
    id = request.GET.get('id')
    try:
        user = TouristaUser.objects.get(id=id)
    except TouristaUser.DoesNotExist:
        return Response(False)
    return Response(UserReturnSerializer(user).data)


@api_view(['POST'])
def createAccount(request):
    serializer = AddUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserReturnSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateData(request, id):
    obj = TouristaUser.objects.get(id=id)
    nationalNumber = request.data.get('nationalNumber')
    try:
        user = TouristaUser.objects.get(nationalNumber=nationalNumber)
        return Response(
            status=status.HTTP_406_NOT_ACCEPTABLE,
            data={
                'errorMessage': 'Duplicate National Number'
            })
    except TouristaUser.DoesNotExist:
        user = None
    data = UpdateDataSerializer(instance=obj, data=request.data)
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
