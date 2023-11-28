import datetime
from django.db import models
# from django.contrib.auth.models import User
from django.forms import DateTimeField
from model_utils.managers import InheritanceManager
from django.contrib.auth.models import AbstractUser
# from enumfields import EnumField
from enum import Enum
from django.conf import settings
# Create your models here.


class TouristaUser(AbstractUser):
    nationalNumber = models.CharField(
        max_length=15, default="", unique=True, blank=False)
    birthDate = models.DateField(blank=False)
    phoneNumber = models.CharField(blank=False, max_length=10)

    REQUIRED_FIELDS = ['nationalNumber', 'birthDate', 'phoneNumber']

    def __str__(self):
        return f"{ self.pk} {self.username}"


class Governate(models.Model):
    name = models.CharField(default='', max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    governateId = models.ForeignKey(
        Governate, on_delete=models.CASCADE, default=None)
    name = models.CharField(default='', max_length=30)

    def __str__(self):
        return self.name


class Street(models.Model):
    cityId = models.ForeignKey(City, on_delete=models.CASCADE, default=None)
    name = models.CharField(default='', max_length=30)

    def __str__(self):
        return self.name


class PublicPlace(models.Model):
    userId = models.ForeignKey(
        TouristaUser, on_delete=models.CASCADE, default=None)
    streetId = models.ForeignKey(
        Street, on_delete=models.CASCADE, default=None)
    isApproved = models.BooleanField(default=False)
    placeType = (
        ('hotel', 'Hotel'),
        ('restaurant', 'Restaurant'),
        ('farm', 'Farm')
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=placeType)
    phoneNumber = models.CharField(max_length=10, default="")
    rating = models.IntegerField(default=1)
    area = models.FloatField(max_length=20, default="")
    # publicPlaceImage= models.ImageField(null=True,blank=True,upload_to='images/')

    class Meta:
        verbose_name_plural = 'public places'

    def __str__(self):
        return self.name


class Hotel(PublicPlace):
    # publicPlaceId = models.OneToOneField(PublicPlace, on_delete=models.CASCADE,related_name="publicPlaceId",default=None)
    # hotel_specific_attribute = models.CharField(max_length=255)
    numberOfRooms = models.IntegerField(default=1)
    numberOfStars = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'hotels'


class Restaurant(PublicPlace):
    openTime = models.TimeField()
    menuType = models.CharField(max_length=500, default="")

    class Meta:
        verbose_name_plural = 'restaurants'


class Table(models.Model):
    tableNumber = models.IntegerField(default=1)


class TableBooking(models.Model):
    price = models.FloatField(max_length=20, default="")
    checkInTime = models.DateTimeField(null=True, blank=True)
    checkoutTime = models.DateTimeField(null=True, blank=True)

# class MenuType(models.Model):
#     restaurantId= models.ForeignKey(Restaurant, on_delete=models.CASCADE,default=None)
#     menuTypeList = (
#         ('Tasting Menu', 'Tasting Menu'),
#         ('Buffet Menu', 'Buffet Menu'),
#         ('Specials Menu', 'Specials Menu'),
#         ('Beverage Menu', 'Beverage Menu'),
#         ('Kids Menu', 'Kids Menu')
#     )
#     menuType= models.CharField(max_length=30,choices=menuTypeList)


class Farm(PublicPlace):
    os_choice = (('daily', 'Daily'),
                 ('monthly', 'Monthly'))
    rentType = models.CharField(max_length=30, choices=os_choice)

    def __str__(self):
        return f'{ self.pk} {self.name} '

    class Meta:
        verbose_name_plural = 'farms'


class Room(models.Model):
    hotelId = models.ForeignKey(Hotel, on_delete=models.CASCADE, default=None)
    roomTypes = (('single', 'single'),
                 ('double', 'double'),
                 ('vipRoom', 'vipRoom'),
                 ('studio', 'studio'))
    roomType = models.CharField(max_length=10, choices=roomTypes, default=None)
    price = models.FloatField(max_length=10, default='')
    roomNumber = models.IntegerField(default=1)
    bedTypes = (('single', 'single'),
                ('double', 'double'))
    bedType = models.CharField(max_length=10, choices=bedTypes)
    area = models.FloatField(max_length=20, default="")
    numberOfPeople = models.IntegerField(default='')


class RoomBooking(models.Model):
    userId = models.ForeignKey(
        TouristaUser, on_delete=models.CASCADE, default=None)
    roomId = models.OneToOneField(
        Room, on_delete=models.CASCADE, related_name="roomId", default=None)

    price = models.FloatField(max_length=20, default="")
    checkInDate = models.DateField(default=datetime.date.today)
    checkoutDate = models.DateField(default=datetime.date.today)


class FarmBooking(models.Model):
    userId = models.ForeignKey(
        TouristaUser, on_delete=models.CASCADE, default=None)
    farmId = models.OneToOneField(Farm, on_delete=models.CASCADE, default=None)

    price = models.FloatField(max_length=20, default="")
    checkInDate = models.DateField(default=datetime.date.today)
    # date=models.TimeField(null=True)
    checkoutDate = models.DateField(default=datetime.date.today)


class Amenities(models.Model):
    placeType = (
        ('hotel', 'Hotel'),
        ('restaurant', 'Restaurant'),
        ('farm', 'Farm')
    )
    type = models.CharField(max_length=20, choices=placeType)
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name
    # freeParking =models.BooleanField(default=False)
    # bar=models.BooleanField(default=False)
    # currencyExchange=models.BooleanField(default=False)
    # twintyFourHoursFrontDesk=models.BooleanField(default=False)
    # carRental=models.BooleanField(default=False)
    # airportDropOff=models.BooleanField(default=False)
    # cleaningServices=models.BooleanField(default=False)
    # laundryServices=models.BooleanField(default=False)
    # dryCleaning=models.BooleanField(default=False)
    # ATM=models.BooleanField(default=False)
    # faxCopyingServices=models.BooleanField(default=False)
    # firstAidServices=models.BooleanField(default=False)
    # wifi=models.BooleanField(default=False)
    # bbq=models.BooleanField(default=False)
    # multiBathrooms=models.BooleanField(default=False)
    # solarHeater=models.BooleanField(default=False)
    # towels=models.BooleanField(default=False)
    # multiRooms=models.BooleanField(default=False)
    # filteredPool=models.BooleanField(default=False)
    # toy=models.BooleanField(default=False)


class Service(models.Model):
    publicPlaceId = models.ForeignKey(
        PublicPlace, on_delete=models.CASCADE, default=None)
    amenityId = models.ForeignKey(
        Amenities, on_delete=models.CASCADE, default=None)


class Images(models.Model):
    publicPlaceId = models.ForeignKey(
        PublicPlace, on_delete=models.CASCADE, default=None)
    path = models.ImageField(blank=True, upload_to='images/')


class TouristDestination(models.Model):
    cityId = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, max_length=15, default=0.0
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, max_length=15, default=0.0
    )
    description = models.CharField(max_length=3000, null=False)

    class Meta:
        verbose_name_plural = "Tourist Destinations"

    def __str__(self):
        return self.name


class TouristDestinationImage(models.Model):
    # TODO:  change the name later
    publicPlaceId = models.ForeignKey(
        TouristDestination, on_delete=models.CASCADE, default=None
    )
    path = models.ImageField(blank=True, upload_to="DestinationImages/")


class Cuisine(models.Model):
    # CuisineList = (
    #     ("Tasting Menu", "Tasting Menu"),
    #     ("Buffet Menu", "Buffet Menu"),
    #     ("Specials Menu", "Specials Menu"),
    #     ("Beverage Menu", "Beverage Menu"),
    #     ("Kids Menu", "Kids Menu"),
    # )
    cuisine = models.CharField(max_length=30)


class RestaurantCuisine(models.Model):
    restaurantId = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, default=None)
    cuisineId = models.ForeignKey(
        Cuisine, on_delete=models.CASCADE, default=None)
