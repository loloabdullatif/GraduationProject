from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.response import Response
from api.serializer import AddUserSerializer, FarmDetailsSerializer, HotelDetailsSerializer, RestaurantDetailsSerializer, UpdateDataSerializer, UserReturnSerializer
from graduationapp.models import Farm, Hotel, PublicPlace, Restaurant, TouristaUser


@api_view(['POST'])
def login(request):
    userName = request.data.get('userName')
    password = request.data.get('password')
    try:
        user = TouristaUser.objects.get(username=userName)
        if user.check_password(password):
            return Response(UserReturnSerializer(user).data)
        else:
            return Response(False)    
    except TouristaUser.DoesNotExist:
        return Response(False)


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
        user.set_password(request.data.get('password'))
        user.save()
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

@api_view(['GET'])
def getMyProperties(request):
    userId= request.GET.get('userId')
    if(userId==None):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    restaurants=Restaurant.objects.filter(userId=userId)
    hotels=Hotel.objects.filter(userId=userId)
    farms=Farm.objects.filter(userId=userId)
    return Response(
        data={
            'hotels':HotelDetailsSerializer(hotels,many=True).data,
            'restaurants':RestaurantDetailsSerializer(restaurants,many=True).data,
            'farms':FarmDetailsSerializer(farms,many=True).data,
        }
    )
    