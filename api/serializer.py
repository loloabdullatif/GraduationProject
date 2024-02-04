
from graduationapp.models import City, Farm, Cuisine, FarmBooking, Governate, PublicPlace, RestaurantCuisine, Room, RoomBooking, Street, Table, TouristDestination, TouristDestinationImage, TouristaUser, Hotel, Amenities, Service, Images, Restaurant
from rest_framework import serializers


class AddUserSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='username')
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')

    class Meta:  # always its name is meta
        model = TouristaUser
        fields = ['userName', 'firstName', 'lastName', 'password',
                  'nationalNumber', 'birthDate', 'phoneNumber']


class UserReturnSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='username')
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    # Modify later when user ownership status is better understood
    isOwner = serializers.BooleanField(default=True)

    class Meta:
        model = TouristaUser
        fields = ['id', 'userName', 'firstName', 'lastName',
                  'nationalNumber', 'birthDate', 'phoneNumber', 'isOwner']


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


class AddRoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = "__all__"


class AvailableReservationRoomSerializer(serializers.ModelSerializer):
    totalPrice = serializers.SerializerMethodField(read_only=True)

    def get_totalPrice(self, room):
        numberOfNights = self.context.get('numberOfNights')
        return numberOfNights*room.price

    class Meta:
        model = Room
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        totalPrice = data.pop('totalPrice')

        return {
            'totalPrice': totalPrice,
            'room': data,
        }


class AddTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class RestaurantDetailsSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)
    cuisines = serializers.SerializerMethodField(read_only=True)

    def get_details(self, restaurant):
        request = self.context.get('request')
        return PublicPlaceDetailsSerializer(restaurant, context={'request': request}).data

    def get_cuisines(self, restaurant):
        restaurantCuisines = RestaurantCuisine.objects.filter(
            restaurantId=restaurant.id)
        cuisines = []
        for restaurantCuisine in restaurantCuisines:
            cuisines.append(restaurantCuisine.cuisineId)
        return CuisineSerializer(cuisines, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)

        location = data.get('details').get('location')
        amenities = data.get('details').get('amenities')
        images = data.get('details').get('images')
        data.pop('details')

        return {
            'location': location,
            'amenities': amenities,
            'images': images,
            'cuisines': data.pop('cuisines'),
            'restaurant': data
        }

    class Meta:
        model = Restaurant
        fields = "__all__"


class FarmDetailsSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)

    def get_details(self, farm):
        request = self.context.get('request')
        return PublicPlaceDetailsSerializer(farm, context={'request': request}).data

    def to_representation(self, instance):
        data = super().to_representation(instance)

        location = data.get('details').get('location')
        amenities = data.get('details').get('amenities')
        images = data.get('details').get('images')
        data.pop('details')

        return {
            'location': location,
            'amenities': amenities,
            'images': images,
            'farm': data
        }

    class Meta:
        model = Farm
        fields = "__all__"


class HotelDetailsSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)

    def get_details(self, hotel):
        request = self.context.get('request')
        return PublicPlaceDetailsSerializer(hotel, context={'request': request}).data

    def to_representation(self, instance):
        data = super().to_representation(instance)

        location = data.get('details').get('location')
        amenities = data.get('details').get('amenities')
        images = data.get('details').get('images')
        data.pop('details')

        return {
            'location': location,
            'amenities': amenities,
            'images': images,
            'hotel': data
        }

    class Meta:
        model = Hotel
        fields = "__all__"


class PublicPlaceDetailsSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    amenities = serializers.SerializerMethodField(read_only=True)

    def get_amenities(self, publicPlace):
        services = Service.objects.filter(publicPlaceId=publicPlace.id)
        amenities = []
        for service in services:
            amenities.append(service.amenityId)

        return AmenitySerializer(amenities, many=True).data

    def get_images(self, hotel):
        request = self.context.get('request')
        imagesObjects = Images.objects.filter(
            publicPlaceId=hotel.id)

        images = []
        for image in imagesObjects:
            # TODO: change this serializer
            images.append(TouristDestinationImageSerializer(
                image, context={'request': request}).data['path'])

        return images

    class Meta:
        model = PublicPlace
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'location': PublicPlaceFullAddressSerializer(instance).data,
            'amenities': data.pop('amenities'),
            'images': data.pop('images'),
        }


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class TouristDestinationBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TouristDestination
        fields = "__all__"


class TouristDestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristDestinationImage
        fields = ['path']


class TouristDestinationDisplaySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    def get_images(self, touristDestination):
        request = self.context.get('request')
        imagesObjects = TouristDestinationImage.objects.filter(
            publicPlaceId=touristDestination.id)

        images = []
        for image in imagesObjects:
            images.append(TouristDestinationImageSerializer(
                image, context={'request': request}).data['path'])

        return images

    class Meta:
        model = TouristDestination
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'images': data.pop('images'),
            'touristDestination': data
        }


class PublicPlaceFullAddressSerializer(serializers.ModelSerializer):
    street = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    governorate = serializers.SerializerMethodField()

    def get_street(self, publicPlace):
        return StreetSerializer(publicPlace.streetId).data

    def get_city(self, publicPlace):
        return CitySerializer(publicPlace.streetId.cityId).data

    def get_governorate(self, publicPlace):
        return GovernorateSerializer(publicPlace.streetId.cityId.governateId).data

    class Meta:
        model = PublicPlace
        fields = ['street', 'city', 'governorate']


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = "__all__"


class RestaurantCuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCuisine
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class AddFarmBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmBooking
        fields = "__all__"


class ReservationRoomSerializer(serializers.ModelSerializer):
    hotel = serializers.SerializerMethodField(read_only=True)
    room = serializers.SerializerMethodField(read_only=True)

    def get_hotel(request, booking):
        return HotelResponseSerializer(booking.roomId.hotelId).data

    def get_room(request, booking):
        return RoomSerializer(booking.roomId).data

    class Meta:
        model = RoomBooking
        fields = "__all__"


class FarmResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farm
        fields = "__all__"


class FarmReservationSerializer(serializers.ModelSerializer):
    farm = serializers.SerializerMethodField(read_only=True)

    def get_farm(request, booking):
        return FarmResponseSerializer(booking.farmId).data

    class Meta:
        model = FarmBooking
        fields = "__all__"


class UserFavoritePropertySerializer(serializers.ModelSerializer):
    object = serializers.SerializerMethodField(read_only=True)

    def get_object(request, property):
        requestContext = request.context.get('request')
        if (property.type == 'hotel'):
            return HotelDetailsSerializer(Hotel.objects.get(id=property.pk), context={'request': requestContext},).data
        if (property.type == 'restaurant'):
            return RestaurantDetailsSerializer(Restaurant.objects.get(id=property.pk), context={'request': requestContext},).data
        return FarmDetailsSerializer(Farm.objects.get(id=property.pk), context={'request': requestContext},).data

    class Meta:
        model = PublicPlace
        fields = ['type', 'id', 'object']
