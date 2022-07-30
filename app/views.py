from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from app.models import  Chat


def index(request):
    friends = User.objects.all()
    context = {'friends': friends}
    return render(request, 'index.html', context)


def detail(request, pk):
    friend = User.objects.get(id=pk)
    room_name = str(int(pk)+int(request.user.id))
    chat = Chat.objects.filter(room_name = room_name)
    return render(request, 'detail.html', context={'friend': friend, 'friend_id': friend.id, 'chat': chat})
