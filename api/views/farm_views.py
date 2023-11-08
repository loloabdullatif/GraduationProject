import json
from typing import Iterable
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.serializer import AddFarmSerializer, ImageSerializer, ServiceSerializer


@api_view(['POST'])
def addFarm(request):
    data = request.data
    farmDict = data.get('farm')
    if farmDict == None:
        return Response(data='No farm was provided', status=status.HTTP_400_BAD_REQUEST)
    if isinstance(farmDict, str):
        farmDict = json.loads(farmDict)
    farmDict['type'] = 'farm'
    amenities = data.get('amenities')
    if amenities == None:
        return Response(data='No amenities were provided', status=status.HTTP_400_BAD_REQUEST)
    if isinstance(amenities, str):
        amenities = json.loads(amenities)
        amenities = [int(i) for i in amenities]
    images = request.FILES
    farmSerializer = AddFarmSerializer(data=farmDict)
    if farmSerializer.is_valid():
        farm = farmSerializer.save()
        publicPlaceId = farm.id

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
    return Response(farmSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
