from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import Chat, Message, Profile

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.core import serializers

from django.contrib.auth.models import User

# from .forms import UploadFileForm
# from somewhere import handle_uploaded_file

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    """
    This is a view to render the chat html.
    """
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [ new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

# def search(q, user_id):
#     uid = User.objects.get(pk=user_id)

def profile_view(request):
    # Felder einfügen Name Alter Wohnort 
    if request.method == 'GET':
        current_user = request.user
        user = User.objects.get(id=current_user.id)
        user_email = user.email
        user_firstname = user.first_name
        return render(request, 'profile/index.html', {'email': user_email, 'firstname': user_firstname}) 
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.file = request.POST.get('profilepicture','')
        profile.save()
        return render(request, 'profile/index.html', {'email': request.user.email, 'file':  profile.file}) 

        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     handle_uploaded_file(request.FILES['file'])
        #     return HttpResponseRedirect('/success/url/')
        # else:
        #     form = UploadFileForm()


def settings_view(request):
    # Felder einfügen Name Alter Wohnort 
    if request.method == 'GET':
        return render(request, 'settings/index.html',)


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