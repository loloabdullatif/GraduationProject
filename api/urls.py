from django.urls import path
from api import views


urlpatterns = [
    path('login/', views.login),
    path('users/getById',views.getById),
    path('signup/', views.signup),
]
