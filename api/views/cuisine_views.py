import json
from typing import Iterable
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
import rest_framework.filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from api.serializer import CuisineSerializer
from graduationapp.models import Cuisine





@api_view(["GET"])
def allCuisines(request):
    cuisines = Cuisine.objects.all()
    return Response(
        status=status.HTTP_200_OK,
        data=CuisineSerializer(cuisines, many=True).data,
    )
    