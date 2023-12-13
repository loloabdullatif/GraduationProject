from django.urls import path
from api.views import room_views
import api.views.auth_views as auth_views
import api.views.hotel_views as hotel_views
import api.views.restaurant_views as restaurant_views
import api.views.farm_views as farm_views
import api.views.locations_views as locations_views
import api.views.amenities_views as amenities_views
import api.views.destinations_views as destinations_views
import api.views.cuisine_views as cuisine_views
# import views as generic_views

urlpatterns = [
    # User & Auth
    path('login/', auth_views.login),
    path('updateData/<int:id>/', auth_views.updateData),
    path('users/getById', auth_views.getById),
    path('createAccount/', auth_views.createAccount),
    # Public Places
    path('myProperties/', auth_views.getMyProperties),
    # Hotels
    path('hotels/', hotel_views.hotels),
    path('hotels/new/', hotel_views.AddHotelAPIView.as_view()),
    path("addRoom/", room_views.addRoom),
    path("hotelsSearch/", hotel_views.HotelSearch.as_view()),
    path("hotels/<int:hotelId>/availableRooms/", hotel_views.getAvailableRooms),
    # path("hotelRooms/", room_views.hotelRooms),

    # Farms
    path('farms/new/', farm_views.addFarm),
    path("allFarms/", farm_views.allFarms),
    path("farmsSearch/", farm_views.FarmSearch.as_view()),

    # Restaurants
    path('restaurants/new/', restaurant_views.addRestaurant),
    path("allRestaurants/", restaurant_views.allRestaurants),
    path("restaurantTables/", restaurant_views.restaurantTables),
    path("addTable/", restaurant_views.addTable),
    path("restaurantsSearch/", restaurant_views.RestaurantSearch.as_view()),

    # Amenities
    path('amenities/', amenities_views.getAmenities),
    # Locations
    path('governorates/', locations_views.getGovernorates),
    path('cities/', locations_views.getCities),
    path('streets/', locations_views.getStreets),
    # Cuisine
    path('cuisines/', cuisine_views.allCuisines),
    # Other
    path('destinations/', destinations_views.getDestinations),


]
