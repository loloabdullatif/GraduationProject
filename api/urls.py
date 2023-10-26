from django.urls import path
from api import views


urlpatterns = [
    path('login/', views.login),
    path('updateData/<int:id>/', views.updateData),
    path('users/getById',views.getById),
    path('createAccount/', views.createAccount),
    path('hotels/', views.addHotel),
    path('amenities/', views.getAmenities),
    path('governorates/', views.getGovernorates),
]
