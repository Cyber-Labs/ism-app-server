from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from club.models import Club
import datetime

class News(models.Model):
    club=models.ForeignKey(Club,on_delete=models.CASCADE)
    news_pic=models.ImageField(upload_to='news_pic',blank=True)
    description=models.CharField(max_length=2000,default='')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description