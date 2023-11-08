from django.urls import path
import api.views.auth_views as auth_views
import api.views.hotel_views as hotel_views
import api.views.restaurant_views as restaurant_views
import api.views.farm_views as farm_views
import api.views.locations_views as locations_views
import api.views.amenities_views as amenities_views
# import views as generic_views

urlpatterns = [
    # User & Auth
    path('login/', auth_views.login),
    path('updateData/<int:id>/', auth_views.updateData),
    path('users/getById', auth_views.getById),
    path('createAccount/', auth_views.createAccount),
    # Hotels
    path('hotels/', hotel_views.hotels),
    path('hotels/new/', hotel_views.AddHotelAPIView.as_view()),
    # Farms
    path('farms/new/', farm_views.addFarm),
    # Restaurants
    path('restaurants/new/', restaurant_views.addRestaurant),
    # Amenities
    path('amenities/', amenities_views.getAmenities),
    # Locations
    path('governorates/', locations_views.getGovernorates),
    path('cities/', locations_views.getCities),
    path('streets/', locations_views.getStreets),
    # Other
]
