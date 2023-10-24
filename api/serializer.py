from graduationapp.models import TouristaUser, Hotel #we need the model we want to serialize
from rest_framework import serializers 

class UserSerializer(serializers.ModelSerializer):
    class Meta:#always its name is meta
        model=TouristaUser
        fields=['id','userName','firstName','lastName','password','isOwner','nationalNumber','birthDate','phoneNumber']
        
class UserReturnSerializer(serializers.ModelSerializer):
    class Meta:#always its name is meta
        model=TouristaUser
        fields=['id','userName','firstName','lastName','isOwner','nationalNumber','birthDate','phoneNumber']    
        
class AddHotelSerializer(serializers.ModelSerializer):
    class Meta:#always its name is meta
        model=Hotel
        fields=['numberOfRooms','area','numberOfStars','phoneNumber','type','name','streetId','userId']
        
        
class UpdateDataSerializer(serializers.ModelSerializer):
    phoneNumber=serializers.CharField( max_length=10)
    firstName=serializers.CharField( max_length=10)
    lastName=serializers.CharField( max_length=10)
    password=serializers.CharField(max_length=10)
    nationalNumber=serializers.CharField(max_length=15)
    birthDate=serializers.DateField()
    class Meta:
        model = TouristaUser
        fields=['firstName','lastName','password','nationalNumber','birthDate','phoneNumber']

        