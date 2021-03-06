from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import RequestContext
from .models import Chat, Message, Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout as auth_logout

# Create your views here.

@login_required(login_url='/login/')
def index(request, name):
    """
    Diese Seite 
    """
    print('recived', name)
    chat_user = User.objects.get(username = name)
    chatuserprofile, created = Profile.objects.get_or_create(user = chat_user)
    # Fehler Abfrage einbauen wenn user Name Falsch ist 
    #django user 
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=chat_user)
        serialized_obj = serializers.serialize('json', [ new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)

    chatMessages = Message.objects.filter(Q(receiver = chat_user, author=request.user) | Q(author = chat_user, receiver=request.user)).order_by('created_at')
    print('FILE IS', chatuserprofile.file)
    return render(request, 'chat/index.html', {'messages': chatMessages, 'chatuser': name, 'profile': chatuserprofile})

# def current_milli_time():
#     return round(time.time() * 1000)

def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect('/settings/')
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})

def register_view(request):
    """
    With the post method, new users can be added by providing such as username, email, password. For the existing Django user model.
    """ 
    if request.method == 'POST': 
        if request.POST.get('password') == request.POST.get('repeated_password'):
            user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'))
            login(request, user)
            return HttpResponseRedirect('/settings/')
        else:
            return render(request, 'auth/register.html') # Todo: Fehlermeldung zur??ckgeben
    return render(request, 'auth/register.html')

# Login functions end
# Pages functions start

def profile_view(request):
    """
    Loads the profile page and using the Get or Post method.
    """
    user = request.user
    profile = ''
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    if request.method == 'GET':
        user_email = user.email
        user_firstname = user.first_name
        user_lastname = user.last_name
        return render(request, 'profile/index.html', {'email': user_email, 'file':  profile.file, 'status': profile.status, 'firstname': user_firstname, 'lastname': user_lastname}) 
    if request.method == 'POST':
        if (request.POST.get('profilstatus')):
            profile.status = request.POST.get('profilstatus')
        print(request.FILES)
        if (request.FILES.get('profilepicture')):
            profile.file = request.FILES.get('profilepicture')
        print(profile.file)
        profile.save()
        return render(request, 'profile/index.html', {'email': request.user.email, 'file':  profile.file, 'status': profile.status, 'firstname': request.user.first_name, 'lastname': request.user.last_name}) 

@login_required(login_url='/login/')
def settings_view(request, exception=None):
    """
    This function returns the settings HTML page and contains a user account delete function.
    """
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.filter(user=user)
    if request.method == 'POST':
        profile.delete()
        User.objects.filter(id=request.user.id).delete()
        return HttpResponseRedirect('/login/')
    if request.method == 'GET':
        return render(request, 'settings/index.html')
    

def logout(request):
    """
    This function logs out the logged in user.
    """
    auth_logout(request)
    return HttpResponseRedirect('/login/')
