from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics,permissions
from news.models import *
from club.models import Club
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
        new=News.objects.create(club=club_obj,description=description,news_pic=news_pic)
        new.save()
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
        new=News.objects.create(club=club_obj,description=description,news_pic=news_pic)
        new.save()
        return JsonResponse({
            'success':True,
            'message':news.nsuccess,
        })

class NewsDelete(APIView):
    """  
    This class is for deleting a existing news.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        news_id=request.GET.get(news_id_)
        news_obj=News.objects.get(id=news_id)
        news_obj.delete()
        return JsonResponse({
            'success':True,
            'message':news.delete,
        })

class NewsList(APIView):
    """  
    This shows the list of all news of all clubs.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        nl=[]
        for i in News.objects.order_by('created_date'):
            club_obj=Club.objects.get(id=i.club_id)
            print(i.news_pic)
            if i.news_pic:
                pic=request.build_absolute_uri(i.news_pic.url)
            else:
                pic=None
            time=i.created_date
            cd=time.strftime('%Y')+'-'+time.strftime('%m')+'-'+time.strftime('%d')
            ct=time.strftime('%H')+':'+time.strftime('%M')+':'+time.strftime('%S')
            nl.append({
                'id':i.id,
                'club_name':club_obj.name,
                'description':i.description,
                'news_pic_url':pic,
                'created_date':cd,
                'created_time':ct,
            })
            print(i.created_date)
        return JsonResponse({
            'success':True,
            'message':news.list,
            'news_list':nl,
        })

class NewsDetails(APIView):
    """
    This provides the details of particular news.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        news_id=request.GET.get(news_id_)
        news_obj=News.objects.get(id=news_id)
        club_obj=Club.objects.get(id=news_obj.club_id)
        if news_obj.news_pic:
            img_url=request.build_absolute_uri(news_obj.news_pic.url)
        else:
            img_url=None

        time=news_obj.created_date
        cd=time.strftime('%Y')+'-'+time.strftime('%m')+'-'+time.strftime('%d')
        ct=time.strftime('%H')+':'+time.strftime('%M')+':'+time.strftime('%S')
        return JsonResponse({
            'success':True,
            'message':clubs.details,
            'club_name':club_obj.name,
            'description':news_obj.description,
            'news_pic_url':img_url,
            'created_date':cd,
            'created_time':ct,
        })

class ClubNews(APIView):
    """
    This class is used for accesing the details of news
    by the paricular club.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        club_id_=request.GET.get(ci)
        nl=[]
        for i in News.objects.order_by('created_date'):
            club_obj=Club.objects.get(id=i.club_id)
            if int(i.club_id)==int(club_id_):
                if i.news_pic:
                    pic=request.build_absolute_uri(i.news_pic.url)
                else:
                    pic=None
                time=i.created_date
                cd=time.strftime('%Y')+'-'+time.strftime('%m')+'-'+time.strftime('%d')
                ct=time.strftime('%H')+':'+time.strftime('%M')+':'+time.strftime('%S')
                nl.append({
                    'id':i.id,
                    'club_name':club_obj.name,
                    'description':i.description,
                    'news_pic_url':pic,
                    'created_date':cd,
                    'created_time':ct,
                })
        return JsonResponse({
            'success':True,
            'message':events.club_event_list,
            'news_list':nl,
        })

