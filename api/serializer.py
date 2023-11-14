
from graduationapp.models import City, Farm, Governate, PublicPlace, Room, Street, Table, TouristaUser, Hotel, Amenities, Service, Images, Restaurant
from rest_framework import serializers



class AddUserSerializer(serializers.ModelSerializer):
    userName = serializers.CharField( source= 'username')
    firstName = serializers.CharField(source= 'first_name')
    lastName = serializers.CharField(source= 'last_name')
    class Meta:  # always its name is meta
        model = TouristaUser
        fields = ['userName', 'firstName', 'lastName', 'password',
                  'nationalNumber', 'birthDate', 'phoneNumber']


class UserReturnSerializer(serializers.ModelSerializer):
    userName = serializers.CharField( source= 'username')
    firstName = serializers.CharField(source= 'first_name')
    lastName = serializers.CharField(source= 'last_name')
    isOwner = serializers.BooleanField(default=True) #Modify later when user ownership status is better understood
    class Meta:  
        model = TouristaUser
        fields = ['id', 'userName', 'firstName', 'lastName',
                   'nationalNumber', 'birthDate', 'phoneNumber','isOwner']


class AddHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['numberOfRooms', 'area', 'numberOfStars',
                  'phoneNumber', 'type', 'name', 'streetId', 'userId']


class UpdateDataSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.CharField(max_length=10)
    firstName = serializers.CharField(max_length=10)
    lastName = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=10)
    nationalNumber = serializers.CharField(max_length=15)
    birthDate = serializers.DateField()

    class Meta:
        model = TouristaUser
        fields = ['firstName', 'lastName', 'password',
                  'nationalNumber', 'birthDate', 'phoneNumber']


class HotelResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['publicPlaceId', 'amenityId']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['publicPlaceId', 'path']


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ['id', 'type', 'name']


class GovernorateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Governate
        fields = '__all__'


class AddRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class AddFarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = '__all__'


class PublicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicPlace
        fields = '__all__'


class AddHotelSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    amenities = serializers.ListField(child=serializers.IntegerField())
    hotel = AddHotelSerializer()

    class Meta:
        model = Hotel
        fields = ('hotel', 'images', 'amenities')

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        amenities_data = validated_data.pop('amenities')
        hotel_data = validated_data.pop('hotel')

        hotel = Hotel.objects.create(**hotel_data)

        for image_data in images_data:
            Images.objects.create(publicPlaceId=hotel, path=image_data)

        for amenity_id in amenities_data:
            amenity = Amenities.objects.get(id=amenity_id)
            service = Service.objects.create(
                publicPlaceId=hotel, amenityId=amenity)

        return hotel



class PublicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicPlace
        fields = "__all__"


class AddRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class AddTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = "__all__"


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"
