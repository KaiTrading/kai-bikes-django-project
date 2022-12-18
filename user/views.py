from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from products.models import Category
from user.models import UserProfile
from home.models import Foot1_Nav, Site_Profile, Top_Nav
from django.http import HttpResponseRedirect
from django.contrib import messages
from user.forms import SignUpForm
# Create your views here.

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login/')
    # Return an 'invalid login' error message.
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    category = Category.objects.all()
    context = {'category': category, 'f1': f1, 'topnav': topnav, 'setting':setting }
    return render(request, 'Accounts/login.html',context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup/')


    form = SignUpForm()
    category = Category.objects.all()
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    context = {'category': category, 'f1': f1, 'topnav': topnav, 'setting':setting,           'form': form }
    return render(request, 'Accounts/signup.html', context)