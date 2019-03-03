from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

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
