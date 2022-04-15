from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Chat, Message, Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

def handler404(request, *args, **argv):
    return redirect('settings')

@login_required(login_url='/login/')
def index(request, name):
    print('recived', name)
    chat_user = User.objects.get(username = name )
    chatuserprofile, created = Profile.objects.get_or_create(user = chat_user)

    """
    This is a view to render the chat html.
    """
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=chat_user)
        serialized_obj = serializers.serialize('json', [ new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)

    chatMessages = Message.objects.filter(Q(receiver = chat_user, author=request.user) | Q(author = chat_user, receiver=request.user)).order_by('created_at')
    print('FILE IS', chatuserprofile.file)
    return render(request, 'chat/index.html', {'messages': chatMessages, 'chatuser': name, 'profile': chatuserprofile})

def login_view(request): 
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            print('request.GET.get(next)', request.GET.get('next'))
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})

def register_view(request):
    # print('DATEN', request.POST) = um die request daten in der Console anzusehen 
    if request.method == 'POST': 
        if request.POST.get('password') == request.POST.get('repeated_password'):
            user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'))
        else:
            return render(request, 'auth/register.html', {'wrongPassword': True}) # Todo: Fehlermeldung zurückgeben
    return render(request, 'auth/register.html', )

# Login functions end
# Pages functions start

def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        user_email = user.email
        user_firstname = user.first_name
        user_lastname = user.last_name
        return render(request, 'profile/index.html', {'email': user_email, 'file':  profile.file, 'firstname': user_firstname, 'lastname': user_lastname, 'status': profile.status}) 
    if request.method == 'POST':
        profile.status = request.POST.get('profilstatus','')
        profile.file = request.POST.get('profilepicture','')
        profile.save()
        return render(request, 'profile/index.html', {'email': request.user.email, 'file':  profile.file, 'status': profile.status}) 

@login_required(login_url='/login/')
def settings_view(request, exception=None):
    if request.method == 'GET':
        return render(request, 'settings/index.html',)

