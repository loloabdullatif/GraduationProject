from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from graduationapp.models import TouristaUser
from api.serializer import UserSerializer
# Create your views here.



@api_view(['POST'])
def login(request):
    userName = request.data.get('userName')
    password = request.data.get('password')
    try:
        user = TouristaUser.objects.get(userName=userName, password=password)
    except TouristaUser.DoesNotExist:
        return Response(False)
    return Response(UserSerializer(user).data)  


@api_view(['GET'])
def getById(request):
    id = request.GET.get('id')
    try:
        user = TouristaUser.objects.get(id=id)
    except TouristaUser.DoesNotExist:
        return Response(False)
    return Response(UserSerializer(user).data)  

@api_view(['POST'])
def signup(request):
    data={
    'userName':request.data.get('userName'),
    'phoneNumber':request.data.get('phoneNumber'),
    'firstName':request.data.get('firstName'),
    'lastName':request.data.get('lastName'),
    'password':request.data.get('password'),
    'nationalNumber':request.data.get('nationalNumber'),
    'birthDate':request.data.get('birthDate'),
    'isOwner':request.data.get('isOwner'),
    }
    serializer= UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

