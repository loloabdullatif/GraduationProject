from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.serializer import AmenitySerializer
from graduationapp.models import Amenities


@api_view(['GET'])
def getAmenities(request):
    amenityType = request.GET.get('type')
    amenities = Amenities.objects.filter(type=amenityType)
    return Response(AmenitySerializer(amenities, many=True).data)
