import json
from typing import Iterable
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
import rest_framework.filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from api.serializer import AddFarmSerializer, AmenitySerializer, FarmDetailsSerializer, ImageSerializer, ServiceSerializer
from graduationapp.models import Farm, Images, Service


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


@api_view(["GET"])
def allFarms(request):
    farms = Farm.objects.all()[:10]
    farmsReturnObject = []
    for farm in farms:
        farmServices = Service.objects.filter(publicPlaceId=farm.id)
        farmAmenities = []
        for farmService in farmServices:
            farmAmenities.append(farmService.amenityId)
        serializedAmenities = AmenitySerializer(farmAmenities, many=True).data
        images = Images.objects.filter(publicPlaceId=farm.id)
        serializerImages = ImageSerializer(
            images,
            many=True,
            context={"request": request},
        ).data
        farmsReturnObject.append(
            {
                "farm": FarmDetailsSerializer(farm).data,
                "amenities": serializedAmenities,
                "images": serializerImages,
            }
        )
        return Response(status=status.HTTP_200_OK, data=farmsReturnObject)

    return Response(
        status=status.HTTP_200_OK,
        data=FarmDetailsSerializer(farms, many=True).data,
    )


class FarmSearch(generics.ListAPIView):
    serializer_class = FarmDetailsSerializer
    queryset = Farm.objects.all()
    filter_backends = [filters.OrderingFilter,
                       filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['rating']
    filterset_fields = ['streetId']
    search_fields = ['name']