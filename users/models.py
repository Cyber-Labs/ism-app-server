from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from club.models import *
from events.models import *
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
        return self.user.username

def create_profile(sender,**kwargs):
    if kwargs['created']:
         user_profile=UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)


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
