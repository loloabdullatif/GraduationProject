import genericpath
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from graduationapp.models import TouristaUser,Hotel
from api.serializer import UpdateDataSerializer, UserSerializer,UserReturnSerializer,AddHotelSerializer
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
    data={
    'userName':request.data.get('userName'),
    'phoneNumber':request.data.get('phoneNumber'),
    'firstName':request.data.get('firstName'),
    'lastName':request.data.get('lastName'),
    'password':request.data.get('password'),
    'nationalNumber':request.data.get('nationalNumber'),
    'birthDate':request.data.get('birthDate'),
    }
    serializer= UserSerializer(data=data)

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




# @api_view(['POST'])
# def addHotel(request):
#     data= request.data.get()
#     serializer= AddHotelSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         amenities= request.data.get('amenities')
#         for (x in amenities):
            
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  