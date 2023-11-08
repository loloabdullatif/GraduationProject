from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializer import CitySerializer, GovernorateSerializer, StreetSerializer

from graduationapp.models import City, Governate, Street


@api_view(['GET'])
def getGovernorates(request):
    id = request.GET.get('id')
    if id != None:
        return getGovernorateById(id)
    governorates = Governate.objects.all()
    return Response(GovernorateSerializer(governorates, many=True).data)


def getGovernorateById(id):
    try:
        amenities = Governate.objects.get(id=id)
    except Governate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(GovernorateSerializer(amenities, many=False).data)


@api_view(['GET'])
def getCities(request):
    id = request.GET.get('id')
    if id != None:
        return getCityById(id)
    governorateId = request.GET.get('governorateId')
    if governorateId != None:
        return getCitiesInGovernorate(governorateId)
    cities = City.objects.all()
    return Response(CitySerializer(cities, many=True).data)


def getCityById(id):
    try:
        city = City.objects.get(id=id)
    except City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(CitySerializer(city, many=False).data)


def getCitiesInGovernorate(governorateId):
    cities = City.objects.filter(governateId=governorateId)
    return Response(CitySerializer(cities, many=True).data)


@api_view(['GET'])
def getStreets(request):
    id = request.GET.get('id')
    if id != None:
        return getStreetById(id)
    cityId = request.GET.get('cityId')
    if cityId != None:
        return getStreetsInCity(cityId)
    streets = Street.objects.all()
    return Response(StreetSerializer(streets, many=True).data)


def getStreetById(id):
    try:
        street = Street.objects.get(id=id)
    except Street.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(StreetSerializer(street, many=False).data)


def getStreetsInCity(cityId):
    streets = Street.objects.filter(cityId=cityId)
    return Response(StreetSerializer(streets, many=True).data)
