# import datetime
from django.db import models
# from django.db.models.fields import DateField
from datetime import date
from django.conf import settings

# import time

# Create your models here.

class Chat(models.Model):    
    created_at = models.DateField(default=date.today)

# class Message extends models.Model
class Message(models.Model): #  class Message extends models.Model
    text = models.CharField(max_length=500) # <input type="text" maxlength="500">
    created_at = models.DateField(default=date.today)
    # milli_sec = int(round(time.time() * 1000))
    # print(milli_sec)
    # timestamp = models.IntegerField(default=milli_sec)

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True) 
    # 4, standartwert ist null 5, erlauben dass es leer sein darf 6, dass die Datenbank Nullwerte akzeptiert
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set')


class Profile(models.Model):
    file = models.FileField(blank=True, null=True, upload_to='static/uploads') # <input type="file"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,) # <select><option> User1</option> ...
    status = models.CharField(max_length=500, blank=True, null=True)

    