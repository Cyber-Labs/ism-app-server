from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics,permissions
from news.models import *
from messages import *
from keys import *
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from rest_framework.authtoken.models import Token
from django.http import HttpResponse,JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from django.core.mail import send_mail,EmailMessage
from random import randint

class PostNews(APIView):
    """  
    This api is for creating news.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        club=request.POST.get(ci)
        description=request.POST.get(desc_)
        news_pic=request.FILES.get(np_)
        #user=request.user
        club_obj=Club.objects.get(id=club)
        news=News.objects.create(club=club_obj,title=title,short_desc=short_desc,description=description,news_pic=news_pic)
        news.save()
        return JsonResponse({
            'success':True,
            'message':news.nsuccess,        
        })

class EditNews(APIView):
    """  
    This api is for  news.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        news_id=request.POST.get(news_id_)
        club=request.POST.get(ci)
        description=request.POST.get(desc_)
        news_pic=request.FILES.get(np_)
        #user=request.user
        club_obj=Club.objects.get(id=club)
        news=News.objects.create(club=club_obj,title=title,short_desc=short_desc,description=description,news_pic=news_pic)
        news.save()
        return JsonResponse({
            'success':True,
            'message':news.esucess,
        })



