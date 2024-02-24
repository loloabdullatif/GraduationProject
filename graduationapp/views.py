from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.template import loader
from graduationapp.models import Farm,PublicPlace,FarmBooking,TouristaUser
from django.db.models import Subquery
# from django.contrib.auth.models import User
#web imports
from audioop import avg, avgpp
import datetime
from pyexpat.errors import messages
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render ,HttpResponseRedirect, get_object_or_404
from django.template import loader
from django.http import  HttpResponse , JsonResponse
from django.views import View
#from userapp import models
from django.views.decorators.csrf import csrf_exempt , csrf_protect
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User , auth
from .models import Cuisine, FarmBooking, RestaurantCuisine, Room, Service, TouristaUser ,  Hotel , PublicPlace ,RoomBooking ,Farm , Restaurant ,Images,Governate,City,Street , Table, TableBooking,Amenities, TouristDestination, TouristDestinationImage
from django.contrib.auth.decorators import login_required
#from .decorators import forAdmin
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime,time  ,timedelta
import json
from django.contrib.auth.hashers import make_password
from django.contrib import messages

# Create your views here.
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# def create_account(request):
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Save the form data to create a new user object
#             # Perform any additional actions, such as sending a confirmation email
#             return redirect('index')  # Replace 'login' with the URL name of your login page
#     else:
#         form = CreateUserForm()
#     return render(request, 'registration.html')# ,{'form': form}

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')  # Replace 'home' with the URL name of your home page
#             else:
#                 form.add_error(None, 'Invalid username or password')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

# def logout(request):
#     return redirect('login')


# def getPendingPublicPlaces(request):
#     publicPlaces = PublicPlace.objects.get(isApproved=False)
#     # TODO: return a proper web page
#     return redirect('login')

#web views
def  index(request):
    images = TouristDestinationImage.objects.all()

    hotel=Hotel.objects.all().count()
    farm=Farm.objects.all().count()
    restaurant=Restaurant.objects.all().count()
    username = request.user.username
    response = render(request,'index.html',{'images': images,'hotel':hotel,'farm':farm,'restaurant':restaurant,'username': username})
    return HttpResponse(response)



@login_required(login_url='login')
def account(request):
    return render(request, 'account.html')


@user_passes_test(lambda u: u.is_superuser)
def adminpage(request):
    publicplace = PublicPlace.objects.all()
    return render(request, 'adminpage.html', {'publicplace': publicplace})
    

@login_required
def approve_place(request, publicplace_id):
    place = get_object_or_404(PublicPlace, id=publicplace_id)
    place.isApproved = True
    place.userId.username = request.user
    place.save()
    return redirect('/adminpage')

@login_required
def reject_place(request, publicplace_id):
    place = get_object_or_404(PublicPlace, id=publicplace_id)
    place.delete()
    return redirect('/adminpage')



def yourplace(request):
    hotels = Hotel.objects.filter(userId=request.user)
    farms = Farm.objects.filter(userId=request.user)
    restaurants = Restaurant.objects.filter(userId=request.user)
    return render(request, 'yourplace.html', {'hotels': hotels,'farms':farms,'restaurants':restaurants})
    


    

def mybooking (request):
    tableb = TableBooking.objects.filter(userId=request.user)
    hotelb = RoomBooking.objects.filter(userId=request.user)
    farmb=FarmBooking.objects.filter(userId=request.user)
    return render(request, 'mybooking.html', {'tableb': tableb, 'hotelb': hotelb,'farmb':farmb})

def delete_mybookingfarm(request, farmbooking_id):
    farmbooking = FarmBooking.objects.get(id=farmbooking_id)
    farm_id=farmbooking.farmId.id
    farmbooking.delete()
    return redirect(f'/allbookings/{farm_id}')   
    

      
def delete_myroombooking(request, roombooking_id):
    roombooking =RoomBooking.objects.get(id=roombooking_id)
    hotel_id = roombooking.roomId.hotelId.id
    roombooking.delete()
    return redirect(f'/allroombookings/{hotel_id}')       
    
def delete_mytablebooking(request, tablebooking_id):
    tablebooking =TableBooking.objects.get(id=tablebooking_id)
    resturent_id=tablebooking.tableId.restaurantId.id
    tablebooking.delete()
    
    return redirect(f'/alltablebookings/{resturent_id}') 
             
def delete_farmbooking(request, farmbooking_id):
    farmbooking = FarmBooking.objects.get(id=farmbooking_id)
    farmbooking.delete()
    
    return redirect('/mybookings')


def delete_roombooking(request, roombooking_id):
    roombooking=RoomBooking.objects.get(id=roombooking_id)
    roombooking.delete()
    return redirect('/mybookings')

def delete_tablebooking(request, tablebooking_id):
    tablebooking=TableBooking.objects.get(id=tablebooking_id)
    tablebooking.delete()
    return redirect('/mybookings')



@csrf_exempt
def registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        nationalNumber = request.POST['nationalNumber']
        phoneNumber = request.POST['phoneNumber']
        birthDate = request.POST['birthDate']

        if password == password2:
            if TouristaUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken!')
                print("Username already taken!")
                return redirect('/registration')
            elif TouristaUser.objects.filter(nationalNumber=nationalNumber).exists():
                messages.error(request, 'National number already exists!')
                print("National number already exists!")
                return redirect('/registration')
            else:
                user = TouristaUser.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                  password=password, nationalNumber=nationalNumber,
                                                  phoneNumber=phoneNumber, birthDate=birthDate)
                user.save()
                #login(request, user)
                messages.success(request, "Registration successful.")
                return redirect('/')
        else:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration.html')

    return render(request, 'registration.html', {'messages': messages.get_messages(request)})

#template = 'login.html'
@csrf_exempt
def  login(request):
    #template = loader.get_template('index.html') 
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=auth.authenticate(username=username,password=password)
        
        if user is not None :
            auth.login(request ,user)
            return redirect('/')
        else:
            # كلمة المرور غير صحيحة
            messages.error(request, "Invalid username or password.")
            
            return render(request, 'login.html')

    return render(request, 'login.html')

def logout_view(request):
   # if request.user
    logout(request)
    return redirect('/')
  



def profile(request):
    username = request.user.username
    return render(request, 'profile.html', {'username': username})

def hotel(request):
   
    hotels = Hotel.objects.filter(isApproved=1)
    #hotels = Hotel.objects.all()
    users=TouristaUser.objects.all()
    
    context = {}
    for hotel in hotels:
        user = hotel.userId
        username = user.username
        images = hotel.images_set.all()

        context[hotel.id] = {"numberOfRooms": hotel.numberOfRooms,
                              "numberOfStars": hotel.numberOfStars,
                              "name":hotel.name,
                              "username":user.username,
                              "hotel_id":hotel.id,
                              "streetId":hotel.streetId,
                              "images": images ,
                              "phoneNumber":hotel.phoneNumber,
                              "cityId":hotel.streetId.cityId,
                              
            
                              }

        
    return render(request=request, template_name="hotel.html", context={"data":context})



@csrf_exempt
@login_required(login_url='login')
def addhotel(request):
    all_governate = Governate.objects.values_list('governateName', 'id').distinct().order_by()
    all_city = City.objects.values_list('cityName', 'id').distinct().order_by()
    amenities = Amenities.objects.filter(type='Hotel')  
    if request.method == 'POST' :
        name = request.POST['name']
        governate_id = request.POST.get('governateName', 'id')
        city_id = request.POST.get('cityName') # ,''
        street_name = request.POST['streetName']
        numberOfRooms=request.POST['numberOfRooms']
        phoneNumber=request.POST['phoneNumber']
        numberOfStars=request.POST['numberOfStars']
        area=request.POST['area']
        facebookLink=request.POST['facebookLink']
        instagramLink=request.POST['instagramLink']
        cancellationPolicy=request.POST['cancellationPolicy']
        policies=request.POST['policies']
        kilometersFromCityCenter=request.POST['kilometersFromCityCenter']
        userId = request.user
        governate = Governate.objects.get(id=governate_id)
        city = City.objects.get(id=city_id, governateId=governate)
        streetId = Street.objects.create(cityId=city, streetName=street_name)
        newHotel = Hotel(streetId=streetId,userId=userId,name=name, numberOfRooms= numberOfRooms,phoneNumber=phoneNumber,numberOfStars= numberOfStars,area=area,facebookLink=facebookLink,instagramLink=instagramLink,cancellationPolicy=cancellationPolicy,policies=policies,kilometersFromCityCenter=kilometersFromCityCenter,isApproved=False)
        newHotel.save()
        publicPlaceId=newHotel
    
        files=request.FILES.getlist('path')
        for i in files:
            image=Images.objects.create(publicPlaceId=publicPlaceId,path =i)
            image.save()
            
        amenity_ids = request.POST.getlist('amenityIds[]')
        
        # حفظ الـ Amenities المحددة في النموذج Service
        for amenity_id in amenity_ids:
            amenity = Amenities.objects.get(id=amenity_id)
            service = Service(publicPlaceId=newHotel, amenityId=amenity)
            service.save()

        messages.success(request,'The request will be reviewed. Please wait for approval')
        return redirect('/addhotel/addroom/'+str(newHotel.id))    

    else:
        response = render(request,'addhotel.html',{'all_governate':all_governate,'all_city':all_city,'amenities': amenities})
        return HttpResponse(response)
    
        
            
        
    
@csrf_exempt
def public_place_detail(request,hotel_id):
        public_place = PublicPlace.objects.get(pk=hotel_id)
        images = public_place.images_set.all()
        amenities=Service.objects.filter(publicPlaceId=hotel_id)
        
   
        context = {
          
            'public_place': public_place,
            'images': images,
            'amenities':amenities,
        }
   
        return render(request, 'detailhotel.html', context)

def public_place_detail2(request,farm_id):
        public_place = PublicPlace.objects.get(pk=farm_id)
        images = public_place.images_set.all()# استرجاع الصور المرتبطة بالمكان العام
        amenities=Service.objects.filter(publicPlaceId=farm_id)
       # average_rating = PublicPlace.objects.filter(pk=farm_id).aggregate(average_rating=avgpp('rating'))['rating']
        context = {
            'public_place': public_place,
            'images': images,
            'amenities':amenities,
          #  'average_rating':average_rating,
        }
   
        return render(request, 'detailfarm.html', context)

def public_place_detail3(request,resturant_id):
        public_place = PublicPlace.objects.get(pk=resturant_id)
        images = public_place.images_set.all()# استرجاع الصور المرتبطة بالمكان العام
        amenities=Service.objects.filter(publicPlaceId=resturant_id)
        context = {
            'public_place': public_place,
            'images': images,
            'amenities':amenities,
        }
   
        return render(request, 'detailres.html', context)




@csrf_exempt
@login_required(login_url='login')
def addfarm(request):
        all_governate =Governate.objects.values_list('governateName','id').distinct().order_by()
        all_city=City.objects.values_list('cityName','id').distinct().order_by()
        # all_street=Street.objects.values_list('streetName','id').distinct().order_by()
        amenities = Amenities.objects.filter(type='Farm')
        if request.method == 'POST' :
            name = request.POST['name']
            governate_id= request.POST.get('governateName','id')
            city_id = request.POST.get('cityName')
            street_name = request.POST['streetName']
            phoneNumber=request.POST['phoneNumber']
            area=request.POST['area']
            facebookLink=request.POST['facebookLink']
            instagramLink=request.POST['instagramLink']
            cancellationPolicy=request.POST['cancellationPolicy']
            policies=request.POST['policies']
            kilometersFromCityCenter=request.POST['kilometersFromCityCenter']
            rentType=request.POST['rentType']
            userId = request.user
            governate = Governate.objects.get(id=governate_id)
            city = City.objects.get(id=city_id, governateId=governate)
            streetId = Street.objects.create(cityId=city, streetName=street_name)
            newFarm = Farm(streetId=streetId,userId=userId,name=name,rentType=rentType,phoneNumber=phoneNumber,area=area,facebookLink=facebookLink,instagramLink=instagramLink,cancellationPolicy=cancellationPolicy,policies=policies,kilometersFromCityCenter=kilometersFromCityCenter)
            newFarm.save()
            publicPlaceId=newFarm
          
            files=request.FILES.getlist('path')
            for i in files:
                image=Images.objects.create(publicPlaceId=publicPlaceId,path =i)
                image.save()

            
            amenity_ids = request.POST.getlist('amenityIds[]')
        
        # حفظ الـ Amenities المحددة في النموذج Service
            for amenity_id in amenity_ids:
                amenity = Amenities.objects.get(id=amenity_id)
                service = Service(publicPlaceId=newFarm, amenityId=amenity)
                service.save()

            messages.success(request,'The request will be reviewed. Please wait for approval')
            return redirect("/farm")

        else:
            response = render(request,'addfarm.html',{'all_governate':all_governate,'all_city':all_city,'amenities': amenities})
            return HttpResponse(response)
    
    
    
    

@login_required(login_url='login')
def addResturant(request):
        all_governate =Governate.objects.values_list('governateName','id').distinct().order_by()
        all_city=City.objects.values_list('cityName','id').distinct().order_by()
        amenities = Amenities.objects.filter(type='Restaurant')
        cuisines = Cuisine.objects.all()
        if request.method == 'POST' :
            governate_id= request.POST.get('governateName','id')
            city_id = request.POST.get('cityName')
            street_name = request.POST['streetName']
            name = request.POST['name']
            openTime= request.POST['openTime']
   
            phoneNumber=request.POST['phoneNumber']
            userId = request.user
            governate = Governate.objects.get(id=governate_id)
            city = City.objects.get(id=city_id, governateId=governate)
            streetId = Street.objects.create(cityId=city, streetName=street_name)
            area=request.POST['area']
            facebookLink=request.POST['facebookLink']
            instagramLink=request.POST['instagramLink']
            cancellationPolicy=request.POST['cancellationPolicy']
            policies=request.POST['policies']
            kilometersFromCityCenter=request.POST['kilometersFromCityCenter']
            newRestaurant = Restaurant(phoneNumber=phoneNumber,streetId=streetId,userId=userId,name=name,openTime=openTime,area=area,facebookLink=facebookLink,instagramLink=instagramLink,cancellationPolicy=cancellationPolicy,policies=policies,kilometersFromCityCenter=kilometersFromCityCenter)
            newRestaurant.save()
            PublicPlaceId=newRestaurant
        #    messages.success(request,'add successfully')
            files=request.FILES.getlist('path')
            for i in files:
                image=Images.objects.create(publicPlaceId=PublicPlaceId,path =i)
                image.save()
            amenity_ids = request.POST.getlist('amenityIds[]')
        
            for amenity_id in amenity_ids:
                amenity = Amenities.objects.get(id=amenity_id)
                service = Service(publicPlaceId=newRestaurant, amenityId=amenity)
                service.save()
                
            cuisine_ids = request.POST.getlist('cuisineIds[]')
        
            for cuisine_id in cuisine_ids:
                cuisine = Cuisine.objects.get(id=cuisine_id)
                restaurantCuisine = RestaurantCuisine(restaurantId=newRestaurant, cuisineId=cuisine)
                restaurantCuisine.save()    

            messages.success(request,'The request will be reviewed. Please wait for approval')

            template = loader.get_template('addtable.html')
            return redirect('/addResturant/addtable/'+str(newRestaurant.id))    

        else:
            response = render(request,'addRestaurant.html',{'all_governate':all_governate,'all_city':all_city,'amenities': amenities , 'cuisines':cuisines})
        return HttpResponse(response)
    


def dashbord(request, hotel_id):
    rooms = Room.objects.filter(hotelId=hotel_id)
    total_rooms = len(rooms)
   
  
    reserved = len(RoomBooking.objects.all())

    hotel = Hotel.objects.values_list('name', 'id').distinct().order_by()

    # التحقق من وجود غرف متاحة قبل القسمة
    if total_rooms > 0:
        availability_percentage = (total_rooms / total_rooms) * 100
    else:
        messages.error(request,'no rooms in this hotel')
        return redirect('/yourplace')

    response = render(request, 'dashbord.html', {'location': hotel, 'reserved': reserved, 'rooms': rooms,
                                                  'total_rooms': total_rooms, 
                                                  
                                                  'availability_percentage': availability_percentage})
    return HttpResponse(response)

@login_required(login_url='login')
@csrf_exempt
def dashbord_Table(request,resturant_id):
    tables = Table.objects.filter(restaurantId=resturant_id)
    total_tables = len(tables)
    reserved = len(TableBooking.objects.all())

    restaurant = Restaurant.objects.values_list('name','id').distinct().order_by()
    
    if total_tables > 0:
        availability_percentage = (total_tables / total_tables) * 100
    else:
        messages.error(request,'no tables in this restaurant')
        return redirect('/yourplace')

    response = render(request,'dashbordTable.html',{'restaurant':restaurant,'reserved':reserved,'tables':tables,'total_tables':total_tables,'availability_percentage': availability_percentage})
    return HttpResponse(response)

 

def farm(request):
    farms = Farm.objects.filter(isApproved=1)
    users=TouristaUser.objects.all()
    #images=Image.objects.all()
    context = {}
    for farm in farms:
        user = farm.userId
        username = user.username
        images = farm.images_set.all()
        
        context[farm.id] = {
                              "name":farm.name,
                              "username":user.username,
                              "farm_id":farm.id,
                              "streetId":farm.streetId,
                              "images":images,
                              "cityId":farm.streetId.cityId,
                              "rentType":farm.rentType,
                              "phoneNumber":farm.phoneNumber,
                            
                              }
        
    return render(request=request, template_name="farm.html", context={"data":context})


def Resturant(request):
        resturants = Restaurant.objects.filter(isApproved=1)
        users=TouristaUser.objects.all()
       
        context = {}
        for resturant in resturants:
            user = resturant.userId
            username = user.username
            images = resturant.images_set.all()

            context[resturant.id] = {
                                "name":resturant.name,
                                "username":user.username,
                                "cityId":resturant.streetId.cityId,
                                "streetId":resturant.streetId,
                                "images":images,
                                "resturant_id":resturant.id,
                                "openTime":resturant.openTime,
                                 "cityId":resturant.streetId.cityId,
                        
                                }

            
        return render(request=request, template_name="Resturant.html", context={"data":context})


    

@csrf_exempt
def table(request,resturant_id):
    restaurant = Restaurant.objects.get(id=resturant_id)
    tables= Table.objects.filter(restaurantId=resturant_id)   
    users=TouristaUser.objects.all()
    #images=Image.objects.all()

    context = {}
    for table in tables:
        
        context[table.id] = {
                
                                
                                "table_id":table.id,
                                "tableNumber": table.tableNumber,
                                "capacity": table.capacity,
                                "tableType":table.tableType,
                                "restaurant":restaurant,
                                }
        
    return render(request=request, template_name="table.html", context={"data":context})

@csrf_exempt
def addtable(request,resturant_id):
    if request.method == "POST":
        restaurant =Restaurant.objects.get(id=resturant_id)
        tableNumber = int(request.POST['tableNumber'])
        capacity=int(request.POST['capacity'])
        tableType=request.POST['tableType']
        new_table = Table.objects.create(
            restaurantId=restaurant,
            tableNumber=tableNumber,
            capacity=capacity,
            tableType=tableType,
          
           
            )
        new_table.save()
        messages.success(request, "add table successfully")
        #
        return HttpResponseRedirect(request.path_info)    

    else:
        return render(request, 'addtable.html')
    
#table booking

def book_table_page(request):
    table = Table.objects.all().get(id=int(request.GET['table_id']))
    return HttpResponse(render(request,'tablebooking.html',{'table':table}))




@login_required(login_url='login')
@csrf_exempt
def tablebooking(request):
    if request.method == "POST":
        table_id = request.POST.get('table_id')
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        
        # تحديد وقت الافتتاح والإغلاق للمطعم
        restaurant = Restaurant.objects.first()  # استبدل بالطريقة المناسبة لاسترداد المطعم المطلوب
        open_time = time(hour=restaurant.openTime.hour, minute=restaurant.openTime.minute)
        close_time = time(hour=23, minute=59, second=59)

        # التحقق من صحة وقت الحجز
        try:
            check_in_time = datetime.strptime(check_in, "%Y-%m-%dT%H:%M")
            check_out_time = datetime.strptime(check_out, "%Y-%m-%dT%H:%M")
            
            current_date = datetime.now()
            
            if check_in_time <= current_date:
                messages.warning(request,"Check-in date must be in the future.")
                return redirect(f'/book-table?table_id={table_id}')
            
            if check_in_time >= check_out_time:
                messages.warning(request,"Check-in date must be before check-out date.")
                return redirect(f'/book-table?table_id={table_id}')
            
            if check_in_time.time() < open_time or check_out_time.time() > close_time:
                messages.warning(request, "Table booking is only available between the restaurants opening and closing times.")
                return redirect(f'/book-table?table_id={table_id}')
             #   raise ValidationError("Table booking is only available between the restaurant's opening and closing times.")
            
            conflicting_bookings = TableBooking.objects.filter(
                Q(tableId__id=table_id) &
                (Q(checkInTime__lte=check_in_time, checkoutTime__gte=check_in_time) |
                Q(checkInTime__lte=check_out_time, checkoutTime__gte=check_out_time) |
                Q(checkInTime__gte=check_in_time, checkoutTime__lte=check_out_time))
            )

            if conflicting_bookings.exists():
                conflicting_booking = conflicting_bookings.first()
                messages.warning(request, f"Sorry, this table is unavailable for booking. It is already booked from {conflicting_booking.checkInTime} to {conflicting_booking.checkoutTime}.")
                return redirect(f'/book-table?table_id={table_id}')
            else:
                currenTouristaUser = request.user.username
                tablebooking = TableBooking()
                table_object = Table.objects.get(id=table_id)
                user_object = TouristaUser.objects.get(username=currenTouristaUser)
                tablebooking.price = 1000
                tablebooking.userId = user_object
                tablebooking.tableId = table_object
                tablebooking.checkInTime = check_in_time
                tablebooking.checkoutTime = check_out_time
                tablebooking.save()

                messages.success(request, "Congratulations! Booking Successful")
                return redirect("/Resturant")

        except ValidationError as e:
            messages.warning(request, str(e))
            return redirect("/Resturant")
    
    else:
        template = loader.get_template('tablebooking.html')
        return HttpResponse(template.render())
    
            
def book_farm_page(request):
    farm = Farm.objects.all().get(id=int(request.GET['farm_id']))
    return HttpResponse(render(request,'farmbooking.html',{'farm':farm}))



@login_required(login_url='login')
@csrf_exempt
def farmbooking(request):
        if request.method == "POST":
            farm_id =request.POST.get('farm_id')
            check_in =request.POST.get('check_in')
            check_out = request.POST.get('check_out')

            conflicting_bookings = FarmBooking.objects.filter(
            Q(farmId__id=farm_id) &
            (Q(checkInDate__lte=check_in, checkoutDate__gte=check_in) |
            Q(checkInDate__lte=check_out, checkoutDate__gte=check_out) |
            Q(checkInDate__gte=check_in, checkoutDate__lte=check_out))
        )
            if conflicting_bookings.exists():
                conflicting_booking = conflicting_bookings.first()
                
                messages.error(request, f"Sorry, this farm is unavailable for booking. It is already booked from {conflicting_booking.checkInDate} to {conflicting_booking.checkoutDate}.")
                return redirect(f'/book-farm?farm_id={farm_id}')
                                
            else:
                try:
                    check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
                    check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
                    
                    if check_in_date >= check_out_date:
                        raise ValidationError("Check-in date must be before check-out date.")
                    currenTouristaUser = request.user.username
                    farmbooking = FarmBooking()
                    farm_object = Farm.objects.get(id=farm_id)
                    user_object = TouristaUser.objects.get(username=currenTouristaUser)
                    farmbooking.userId = user_object
                    farmbooking.farmId = farm_object
                    farmbooking.price = 1000
                    farmbooking.checkInDate = request.POST['check_in']
                    farmbooking.checkoutDate = request.POST['check_out']
                    farmbooking.save()

                    messages.success(request, "Congratulations! Booking Successful")
                    return redirect("/farm")
            
                except ValidationError as e:
                    messages.warning(request, str(e))
                        # return redirect("farm")

        else:
            template = loader.get_template('farmbooking.html')
            return HttpResponse(template.render())
           
       

@csrf_exempt
def room(request,hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    rooms= Room.objects.filter(hotelId=hotel_id)   
    users=TouristaUser.objects.all()
    #images=Image.objects.all()

    context = {}
    for room in rooms:
        
        context[room.id] = {
                "roomType": room.roomType,
                                
                                "room_id":room.id,
                                "bedType": room.bedType,
                                "price":room.price,
                                "area":room.area,
                                "roomNumber":room.roomNumber,
                                "numberOfPeople":room.numberOfPeople,
                                "hotel_id":hotel,
                                
                                
                                # "path":images.path,
                                
                                }
       
    return render(request=request, template_name="room.html", context={"data":context})




def book_room_page(request):
    room = Room.objects.all().get(id=int(request.GET['room_id']))
    return HttpResponse(render(request,'roombooking.html',{'room':room}))



@login_required(login_url='login')
@csrf_exempt
def roombooking(request):
    if request.method == "POST":
        room_id = request.POST.get('room_id')
        price = request.POST.get('price')
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']

        # التحقق من توفر الغرفة للحجز في التواريخ المحددة
        conflicting_bookings = RoomBooking.objects.filter(
            Q(roomId__id=room_id) &
            (Q(checkInDate__lte=check_in, checkoutDate__gte=check_in) |
            Q(checkInDate__lte=check_out, checkoutDate__gte=check_out) |
            Q(checkInDate__gte=check_in, checkoutDate__lte=check_out))
        )

        if conflicting_bookings.exists():
            conflicting_booking = conflicting_bookings.first()
            messages.warning(request, f"Sorry, this room is unavailable for booking. It is already booked from {conflicting_booking.checkInDate} to {conflicting_booking.checkoutDate}.")
            return redirect(f'/book-room?room_id={room_id}')
             
        else:
            try:
                check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
                check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
                
                if check_in_date >= check_out_date:
                    raise ValidationError("Check-in date must be before check-out date.")
                currenTouristaUser = request.user.username
                #  total_person = int(request.POST['numberOfPeople'])
                bookingroom = RoomBooking()
                room_object = Room.objects.get(id=room_id)
                room_object.status = '2'
                user_object = TouristaUser.objects.get(username=currenTouristaUser)
                # user_object = TouristaUser.objects.get(price=currenTouristaUser)
                bookingroom.userId = user_object
                bookingroom.roomId = room_object
                # numberOfPeople = total_person
                # price1=Room.objects.get(price=1000)
                bookingroom.price = 1000
                bookingroom.checkInDate = request.POST['check_in']
                bookingroom.checkoutDate = request.POST['check_out']
                # bookingroom.price = request.Get('price')
                bookingroom.save()

                messages.success(request, "Congratulations! Booking Successful")

                return redirect('/hotel')
        
            except ValidationError as e:
                messages.warning(request, str(e))
                    # return redirect("room")

    else:
        template = loader.get_template('roombooking.html')
        return HttpResponse(template.render())
    
    
    



@csrf_exempt
def addroom(request,hotel_id):
    if request.method == "POST":
        total_rooms = len(Room.objects.all())
        new_room = Room()
    
        hotel = Hotel.objects.get(id=hotel_id)
        roomNumber = total_rooms + 1
        roomType = request.POST['roomType']
        roomNumber = int(request.POST['roomNumber'])
        price   = int(request.POST['price'])
        area   = int(request.POST['area'])
        numberOfPeople   = int(request.POST['numberOfPeople'])
        # status     = request.POST['status']
        bedType      = request.POST['bedType']
        
        new_room = Room.objects.create(
            hotelId=hotel,
            roomNumber=roomNumber,
            roomType=roomType,
            price=price,
            area =area,
            numberOfPeople=numberOfPeople,
            # status=status,
            bedType=bedType
            )
        new_room.save()
        messages.success(request, "add room successfully")
        # return redirect('addroom/'+str(hotel_id))
        return HttpResponseRedirect(request.path_info)    

    else:
        return render(request, 'addroom.html')

        
    

@csrf_exempt
def updateinfo(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST['username']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        phoneNumber = request.POST['phoneNumber']

        if user.username != username:
            user.username = username
            # user.save()

        if old_password and new_password and confirm_password:
            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    # user.save()
                else:
                    messages.error(request, "New password and confirm password do not match.")
                    return redirect('/updateinfo')
            else:
                messages.error(request, "Old password is incorrect.")
                return redirect('/updateinfo')

        user.phoneNumber = phoneNumber
        user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('/')

    return render(request, 'updateinfo.html', {'user': request.user})


    
def delete_room(request,roomid):
    room=Room.objects.get(id=roomid)
    room.delete()
    return redirect('/')

def delete_table(request,tableid):
    table=Table.objects.get(id=tableid)
    table.delete()
    return redirect('/')



def deletepublicplace(request, publicplace_id):
    publicplace=PublicPlace.objects.get(id=publicplace_id)
    publicplace.delete()
    return redirect('/yourplace')


def allbookings(request, farm_id):
    farm = Farm.objects.get(id=farm_id)
    bookings = FarmBooking.objects.filter(farmId=farm)

    context = {
        'farm': farm,
        'fbookings': bookings,
    }

    return render(request, 'allbooking.html', context)





def allroombookings(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    room =  Room.objects.all()
    bookings = RoomBooking.objects.filter(roomId__in=room)
    context = {
        'hotel':hotel,
        'room': room,
        'bookings': bookings,
    }

    return render(request, 'allbooking.html', context)



def alltablebookings(request, rest_id):
    rest = Restaurant.objects.get(id=rest_id)
    table = Table.objects.filter(rest=rest)
    bookings = TableBooking.objects.all()

    context = {
        'rest':rest,
        'table': table,
        'boookings': bookings,
    }

    return render(request, 'allbooking.html', context)

def proposedplaces(request):
    all_governate =Governate.objects.values_list('governateName','id').distinct().order_by()
    all_city=City.objects.values_list('cityName','id').distinct().order_by()
    if request.method == 'POST':
        governate_name = request.POST.get('governateName')
        city_name = request.POST.get('cityName')
        name = request.POST['name']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        description = request.POST['description']
        governate = Governate.objects.get(id=governate_name)
        city = City.objects.get(id=city_name, governateId=governate)
        # استخدم قيمة المدينة المحددة في إنشاء كائن TouristDestination
        proposed_place = TouristDestination(cityId=city, name=name, latitude=latitude, longitude=longitude, description=description)
        proposed_place.save()
        
        publicPlaceId = proposed_place
        messages.success(request, 'تمت الإضافة بنجاح')
        files = request.FILES.getlist('path')
        for i in files:
            image = TouristDestinationImage.objects.create(publicPlaceId=publicPlaceId, path=i)
            image.save()
        
        # قم بتنفيذ الإجراءات اللازمة مثل إرسال رسالة تأكيد أو تحويل المستخدم إلى صفحة أخرى
        return redirect('/')  # استبدل '/' بعنوان URL الصحيح
 
    
    return render(request, 'proposedPlaces.html', {'all_governate':all_governate,'all_city':all_city})

    
def DeleteAccount(request):
    user = request.user
    user.delete()
    messages.success(request,'Your Account Has Deleted')
    return redirect('/')
