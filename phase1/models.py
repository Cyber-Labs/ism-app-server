from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your models here.

class WelcomeModel(models.Model):
    version=models.IntegerField(default=0)
    is_cumpulsory_update=models.BooleanField(default=False)

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    otp=models.CharField(max_length=13,default='')
    name=models.CharField(max_length=100,default='')

    def __str__(self):
        return self.name

def create_profile(sender,**kwargs):
    if kwargs['created']:
         user_profile=UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)

class Club(models.Model):
    name=models.CharField(max_length=100,default='')
    club_pic=models.ImageField(upload_to='club_pic',blank=True)
    description=models.TextField(max_length=1000,default='')
    tagline=models.CharField(max_length=100,default='')
    club_email=models.EmailField(max_length=100,blank=True, null= True, unique= True)
    fb_link=models.URLField(default='')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ClubMember(models.Model):
    club=models.ForeignKey(Club,on_delete=models.CASCADE)
    app_user=models.ForeignKey(User,on_delete=models.CASCADE)
    is_admin=models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.club.name

class ClubFollower(models.Model):
    club=models.ForeignKey(Club,on_delete=models.CASCADE)
    app_user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.club.name

class News(models.Model):
    club=models.ForeignKey(Club,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,default='')
    news_pic=models.ImageField(upload_to='news_pic',blank=True)
    short_desc=models.CharField(max_length=500,default='')
    description=models.CharField(max_length=2000,default='')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    club=models.ForeignKey(Club,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,default='')
    event_pic=models.ImageField(upload_to='event_pic',blank=True)
    short_desc=models.CharField(max_length=500,default='')
    description=models.CharField(max_length=2000,default='')
    venue=models.CharField(max_length=2000,default='')
    event_start_date = models.DateField(default=datetime.date.today)
    event_end_date = models.DateField(default=datetime.date.today)
    is_active=models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title