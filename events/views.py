from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics,permissions
from .models import *
from messages import *
from keys import *
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from rest_framework.authtoken.models import Token
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage
from django.urls import reverse_lazy
import random
import json

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
        club_obj=Club.objects.get(id=club)
        print(club_obj.id)
        event=Event.objects.create(club=club_obj,title=title,short_desc=short_desc,description=description,venue=venue,event_pic=event_pic,event_start_date=event_start_date,event_end_date=event_end_date)
        event.save()
        return JsonResponse({'message':events.ecsuccess})

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
            'club_list':el,
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