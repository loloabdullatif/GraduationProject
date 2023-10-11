from graduationapp.models import TouristaUser #we need the model we want to serialize
from rest_framework import serializers 

class UserSerializer(serializers.ModelSerializer):
    class Meta:#always its name is meta
        model=TouristaUser
        fields=['id','userName','firstName','lastName','isOwner','nationalNumber','birthDate','phoneNumber']     #fields we want to serialize from object python to json    