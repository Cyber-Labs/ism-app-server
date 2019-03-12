from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics,permissions
from events.models import Event
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

class CreateEvent(APIView):
    """  
    This allows the admin of club to add a event.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        club=request.POST.get(ci)
        title=request.POST.get(title_)
        short_desc=request.POST.get(sd_)
        description=request.POST.get(desc_)
        venue=request.POST.get(venue_)
        event_pic=request.FILES.get(ep_)
        event_start_date=request.POST.get(esd_)
        event_end_date=request.POST.get(eed_)
        if event_end_date is None:
            event_end_date=event_start_date
        club_obj=Club.objects.get(id=club)
        print(club_obj.id)
        event=Event.objects.create(club=club_obj,title=title,short_desc=short_desc,description=description,venue=venue,event_pic=event_pic,event_start_date=event_start_date,event_end_date=event_end_date)
        event.save()
        return JsonResponse({
            'success':True,
            'message':events.ecsuccess
            })

class EditEvent(APIView):
    """  
    This allows the admin of club to edit a event.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        event_id=request.POST.get(event_id_)
        club=request.POST.get(ci)
        title=request.POST.get(title_)
        short_desc=request.POST.get(sd_)
        description=request.POST.get(desc_)
        venue=request.POST.get(venue_)
        event_pic=request.FILES.get(ep_)
        event_start_date=request.POST.get(esd_)
        event_end_date=request.POST.get(eed_)
        club_obj=Club.objects.get(id=club)
        event_obj=Event.objects.get(id=event_id)
        event_obj.club=club_obj
        event_obj.title=title
        event_obj.short_desc=short_desc
        event_obj.description=description
        event_obj.venue=venue
        event_obj.event_pic=event_pic
        event_obj.event_start_date=event_start_date
        event_obj.event_end_date=event_end_date
        event_obj.save()
        return JsonResponse({
            'success':True,
            'message':events.ecsuccess
            })

class ClubEvent(APIView):
    """
    This class is used for accesing the details of events organised
    by the paricular club.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        club_id_=request.GET.get(ci)
        el=[]
        for i in Event.objects.order_by('event_start_date'):
            club_obj=Club.objects.get(id=i.club_id)
            if int(i.club_id)==int(club_id_):
                el.append({
                    'id':i.id,
                    'club_name':club_obj.name,
                    'title':i.title,
                    'short_desc':i.short_desc,
                    'description':i.description,
                    'venue':i.venue,
                    'event_pic_url':request.build_absolute_uri(i.event_pic.url),
                    'event_start_date':i.event_start_date,
                    'event_end_date':i.event_end_date,
                })
        return JsonResponse({
            'success':True,
            'message':events.club_event_list,
            'event_list':el,
        })


class EventDelete(APIView):
    """  
    This class is for deleting a existing event.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        event_id=request.GET.get(event_id_)
        event_obj=Event.objects.get(id=event_id)
        event_obj.delete()
        return JsonResponse({
            'success':True,
            'message':events.delete
        })

class EventList(APIView):
    """  
    This shows the list of all events of all clubs.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        el=[]
        for i in Event.objects.order_by('event_start_date'):
            club_obj=Club.objects.get(id=i.club_id)
            el.append({
                'id':i.id,
                'club_name':club_obj.name,
                'title':i.title,
                'short_desc':i.short_desc,
                'description':i.description,
                'venue':i.venue,
                'event_pic_url':request.build_absolute_uri(i.event_pic.url),
                'event_start_date':i.event_start_date,
                'event_end_date':i.event_end_date,
            })
        return JsonResponse({
            'success':True,
            'message':events.list,
            'event_list':el,
        })

class EventDetails(APIView):
    """
    This provides the details of particular event.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        event_id=request.GET.get(event_id_)
        event_obj=Event.objects.get(id=event_id)
        club_obj=Club.objects.get(id=event_obj.club_id)
        img_url=request.build_absolute_uri(event_obj.event_pic.url)
        return JsonResponse({
            'success':True,
            'message':clubs.details,
            'club_name':club_obj.name,
            'title':event_obj.title,
            'short_desc':event_obj.short_desc,
            'description':event_obj.description,
            'venue':event_obj.venue,
            'event_pic_url':img_url,
            'event_start_date':event_obj.event_start_date,
            'event_end_date':event_obj.event_end_date,
        })

