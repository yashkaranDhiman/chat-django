from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .models import *
# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.all()
    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(desc__icontains=q) |
        Q(name__icontains=q)
        )
    if(q == "all"):
        main_messages = message.objects.all()
        room = Room.objects.all()
    room_count = room.count()
    main_messages = message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':room,'topics':topics,'room_count':room_count,'main_messages':main_messages}
    return render(request,"base/home.html",context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        body = request.POST.get('body')
        messagee = message.objects.create(
            user=request.user,room=room,body=body
            )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,"base/room.html",context) 
    
@login_required(login_url='login')
def createRoom(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect("/")
    form = RoomForm()
    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def roomUpdate(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    
    if request.user != room.host:
        return HttpResponse("sorryyyyyyyyyyyyy")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form':form}
    return render(request,'base/room_form.html',context)
 
def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    main_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'main_messages':main_messages,'topics':topics}
    return render(request,'base/profile.html', context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("/")
    return render(request,'base/delete.html')

def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User does not exist")
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.error(request,"Username or password does not exist")
    context = {'page':page}
    return render(request,'base/login_register.html',context)

def registerUser(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("/")
        else:
            messages.error(request,'an error occured during registration')
    context = {'form':form}
    return render(request,'base/login_register.html',context)

def logout_user(reqeust):
    logout(reqeust)
    return redirect("/")

@login_required(login_url='login')
def deleteComment(request,pk):
    mssg = message.objects.get(id=pk)

    if request.user != mssg.user:
        return HttpResponse("you are not allowed here")

    if request.method =="POST":
        mssg.delete()
        return redirect("/")
    return render(request,'base/delete.html', {'obj':mssg})

def friends(request):
    all_friends = User.objects.all()
    context = {'all_friends':all_friends}
    return render(request,'base/friends.html',context)