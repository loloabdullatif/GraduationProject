from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from graduationapp.models import PublicPlace
from api.serializer import AddHotelSerializer, PublicPlaceSerializer
import rest_framework.filters as filters
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser


class AddHotelView(generics.CreateAPIView):
    parser_class = [MultiPartParser, FormParser]


serializer_class = AddHotelSerializer


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


class PublicPlaceList(generics.ListAPIView):
    serializer_class = PublicPlaceSerializer
    queryset = PublicPlace.objects.all()
    filter_backends = [filters.OrderingFilter,
    filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'numberOfStars']
    filterset_fields = ['streetId']
    search_fields = ['name']


def getString(param):
    return str(param)


class AddHotelAPIView(APIView):
    def post(self, request):
        serializer = AddHotelSerializer(data=request.data)
        if serializer.is_valid():
            hotel = serializer.save()
            return Response({'message': 'Data inserted successfully'})
        return Response(serializer.errors, status=400)
