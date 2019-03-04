from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from club.models import *
from users.models import *
import datetime

# Create your models here.
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