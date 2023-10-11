from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.template import loader
from graduationapp.models import Farm,PublicPlace,FarmBooking,TouristaUser
from django.db.models import Subquery
# from django.contrib.auth.models import User


# Create your views here.
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def create_account(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the form data to create a new user object
            # Perform any additional actions, such as sending a confirmation email
            return redirect('index')  # Replace 'login' with the URL name of your login page
    else:
        form = CreateUserForm()
    return render(request, 'create_account.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Replace 'home' with the URL name of your home page
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    return redirect('login')


def getPendingPublicPlaces(request):
    publicPlaces = PublicPlace.objects.get(isApproved=False)
    # TODO: return a proper web page
    return redirect('login')
