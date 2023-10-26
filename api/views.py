import genericpath
import json
from typing import Iterable
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from graduationapp.models import Amenities, Governate, TouristaUser,Hotel
from api.serializer import AddFarmSerializer, AddRestaurantSerializer, GovernorateSerializer, UpdateDataSerializer, AddUserSerializer,UserReturnSerializer,AddHotelSerializer,ServiceSerializer,ImageSerializer,AmenitySerializer
# Create your views here.



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
    serializer= AddUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# class UpdateData(genericpath.UpdateAPIView):
#     queryset = TouristaUser.objects.all()
#     serializer_class = UpdateDataSerializer
#     #permission_classes = (permissions.IsAuthenticated,)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.name = request.data.get("firstName")
#         instance.save()

#         serializer = self.get_serializer(instance)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         return Response(serializer.data)


@api_view(['PUT'])
def updateData(request, id):
    obj = TouristaUser.objects.get(id=id)
    nationalNumber= request.data.get('nationalNumber')
    try:
        user = TouristaUser.objects.get(nationalNumber=nationalNumber)
        return Response(
            status=status.HTTP_406_NOT_ACCEPTABLE,
            data={
            'errorMessage':'Duplicate National Number'
        })
    except TouristaUser.DoesNotExist:
        user = None
    data = UpdateDataSerializer(instance=obj, data=request.data)
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)



# Things we need from the front-end:
# 1. The public place object
# 2. The related amenities
# 3. The images
@api_view(['POST'])
def addHotel(request):
    data= request.data
    hotelDict = data.get('hotel')
    if isinstance(hotelDict, str):
        hotelDict = json.loads(hotelDict)
    amenities = data.get('amenities')
    if isinstance(amenities, str):
        amenities = json.loads(amenities)
        amenities = [int(i) for i in amenities]
    images=request.FILES
    hotelSerializer= AddHotelSerializer(data=hotelDict)
    if hotelSerializer.is_valid():
        hotel= hotelSerializer.save()
        publicPlaceId= hotel.id
        
        if isinstance(amenities, Iterable):
            for amenityId in amenities:
                serviceSerializer = ServiceSerializer(data={
                    'publicPlaceId':publicPlaceId,
                    'amenityId': amenityId,
                })
                if serviceSerializer.is_valid():
                    serviceSerializer.save()
                else:
                    return Response(serviceSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        if isinstance(images, Iterable):    
            for imageKey in images.keys():
                imageSerializer = ImageSerializer(data={
                    'publicPlaceId':publicPlaceId,
                    'path': images[imageKey],
                })
                if imageSerializer.is_valid():
                    imageSerializer.save()
                else:
                    return Response(imageSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        return Response(True,status=status.HTTP_201_CREATED)
    return Response(hotelSerializer.errors,status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
def getAmenities(request):
    amenityType=request.GET.get('type')
    amenities=Amenities.objects.filter(type=amenityType)
    return Response(AmenitySerializer(amenities,many =True).data)

@api_view(['GET'])
def getGovernorates(request):
    id = request.GET.get('id')
    if id != None:
        return getGovernorateById(id)
    governorates=Governate.objects.all()
    return Response(GovernorateSerializer(governorates,many =True).data)


def getGovernorateById(id):
    try:
        amenities=Governate.objects.get(id=id)
    except Governate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(GovernorateSerializer(amenities,many =False).data)


@api_view(['POST'])
def addRestaurant(request):
    data= request.data
    restaurantDict = data.get('restaurant')
    if isinstance(restaurantDict, str):
        restaurantDict = json.loads(restaurantDict)
    amenities = data.get('amenities')
    if isinstance(amenities, str):
        amenities = json.loads(amenities)
        amenities = [int(i) for i in amenities]
    images=request.FILES
    restaurantSerializer= AddRestaurantSerializer(data=restaurantDict)
    if restaurantSerializer.is_valid():
        restaurant= restaurantSerializer.save()
        publicPlaceId= restaurant.id
        
        if isinstance(amenities, Iterable):
            for amenityId in amenities:
                serviceSerializer = ServiceSerializer(data={
                    'publicPlaceId':publicPlaceId,
                    'amenityId': amenityId,
                })
                if serviceSerializer.is_valid():
                    serviceSerializer.save()
                else:
                    return Response(serviceSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        if isinstance(images, Iterable):    
            for imageKey in images.keys():
                imageSerializer = ImageSerializer(data={
                    'publicPlaceId':publicPlaceId,
                    'path': images[imageKey],
                })
                if imageSerializer.is_valid():
                    imageSerializer.save()
                else:
                    return Response(imageSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        return Response(True,status=status.HTTP_201_CREATED)
    return Response(restaurantSerializer.errors,status=status.HTTP_400_BAD_REQUEST)  

@api_view(['POST'])
def addFarm(request):
    data= request.data
    farmDict = data.get('farm')
    if isinstance(farmDict, str):
        farmDict = json.loads(farmDict)
    amenities = data.get('amenities')
    if isinstance(amenities, str):
        amenities = json.loads(amenities)
        amenities = [int(i) for i in amenities]
    images=request.FILES
    farmSerializer= AddFarmSerializer(data=farmDict)
    if farmSerializer.is_valid():
        farm= farmSerializer.save()
        publicPlaceId= farm.id
        
        if isinstance(amenities, Iterable):
            for amenityId in amenities:
                serviceSerializer = ServiceSerializer(data={
                    'publicPlaceId':publicPlaceId,
                    'amenityId': amenityId,
                })
                if serviceSerializer.is_valid():
                    serviceSerializer.save()
                else:
                    return Response(serviceSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        if isinstance(images, Iterable):    
            for imageKey in images.keys():
                imageSerializer = ImageSerializer(data={
                    'publicPlaceId':publicPlaceId,
                    'path': images[imageKey],
                })
                if imageSerializer.is_valid():
                    imageSerializer.save()
                else:
                    return Response(imageSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        return Response(True,status=status.HTTP_201_CREATED)
    return Response(farmSerializer.errors,status=status.HTTP_400_BAD_REQUEST)  