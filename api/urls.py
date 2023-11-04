from django.urls import path
from api import views


urlpatterns = [
    path('login/', views.login),
    path('updateData/<int:id>/', views.updateData),
    path('users/getById',views.getById),
    path('createAccount/', views.createAccount),
    path('hotels/', views.hotels),
    # path('addHotel/', views.addHotel),
    path('farms/', views.addFarm),
    path('restaurants/', views.addRestaurant),
    path('amenities/', views.getAmenities),
    path('governorates/', views.getGovernorates),
    path('cities/', views.getCities),
    path('streets/', views.getStreets),
    path('places/', views.PublicPlaceList.as_view()),
]
