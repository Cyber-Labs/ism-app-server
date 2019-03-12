from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics,permissions
from club.models import Club,ClubMember,ClubFollower
from users.models import UserProfile
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


class ClubList(APIView):
    """  
    This class is for showing all the club list.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)

    def get(self,request,*args,**kwargs):
        cl=[]
        for i in Club.objects.all():
            cl.append({
                'id':i.id,
                'name':i.name,
                'image_url':request.build_absolute_uri(i.club_pic.url),
                'tagline':i.tagline
            })
        return JsonResponse({
            'success':True,
            'message':clubs.details,
            'club_list':cl,
        })


class ClubDetails(APIView):
    """  
    This class is for showing the detail of a specific club.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)

    def get(self,request,*args,**kwargs):
        club=request.GET.get(ci)
        club_obj=Club.objects.get(id=club)
        user=request.user
        try:
            cm=ClubMember.objects.get(club=club_obj,app_user=user)
            im=cm.is_admin
        except ClubMember.DoesNotExist:
            im=False
        img_url=request.build_absolute_uri(club_obj.club_pic.url)
        return JsonResponse({
            'success':True,
            'message':clubs.details,
            'id':club_obj.id,
            'name':club_obj.name,
            'image_url':img_url,
            'tagline':club_obj.tagline,
            'description':club_obj.description,
            'fb_link':club_obj.fb_link,
            'is_admin':im
        })


class ClubMemberList(APIView):
    """  
    This class is for showing the member list of a specific club.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)

    def get(self,request,*args,**kwargs):
        club=request.GET.get(ci)
        club_obj=Club.objects.get(id=club)
        user=request.user
        cm=list(ClubMember.objects.filter(club=club_obj).values())
        u=[]
        for i in range(len(cm)):
            u.append(cm[i]['app_user_id'])
        ml=[]
        for i in u:
            x=User.objects.get(id=i).email
            y=UserProfile.objects.get(user_id=i).name
            z=ClubMember.objects.get(app_user=i,club=club_obj).is_admin
            ml.append({
                'email':x,
                'name':y,
                'is_admin':z
            })
        print(ml)
        return JsonResponse({
            'success':True,
            'message':clubs.member,
            'member_list':ml,
        })


class AddClubMembers(APIView):
    """  
    This class provide the access of adding a member in a club to the admin
    of clubs.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)

    def get(self,request,*args,**kwargs):
        club=request.GET.get(ci)
        app_user=request.GET.get(ei)
        is_admin=request.GET.get(ia)
        if is_admin=='true':
            is_admin=True
        if is_admin=='false':
            is_admin=False
        try:
            user=User.objects.get(username=app_user)
        except User.DoesNotExist:
            user=False
        if user==False:
            return JsonResponse({
                'success':False,
                'message':clubs.not_exist,
            })
        club_obj=Club.objects.get(id=club)
        try:
            cm=ClubMember.objects.get(club=club_obj,app_user=request.user).is_admin
        except ClubMember.DoesNotExist:
            cm=False
        if cm == False:
            return JsonResponse({
                'success':False,
                'message':clubs.amfailure,
            })
        if ClubMember.objects.filter(club=club_obj,app_user=user).count()!=0:
            return JsonResponse({
                'success':True,
                'message':clubs.amalready,
            })
        member=ClubMember.objects.create(club=club_obj,app_user=user,is_admin=is_admin)
        member.save()
        return JsonResponse({
            'success':True,
            'message':clubs.amsuccess
        })


class RemoveClubMembers(APIView):
    """  
    This class allows the admin of clubs to remove members from club.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        club=request.GET.get(ci)
        app_user=request.GET.get(ei)
        user=User.objects.get(username=app_user)
        club_obj=Club.objects.get(id=club)
        try:
            cm=ClubMember.objects.get(club=club_obj,app_user=request.user).is_admin
        except ClubMember.DoesNotExist:
            cm=False
        if cm == False:
            return JsonResponse({
                'success':False,
                'message':clubs.rmfailure
            })
        member=ClubMember.objects.get(club=club_obj,app_user=user)
        member.delete()
        return JsonResponse({
            'success':True,
            'message':clubs.rmsuccess
        })

class FollowClub(APIView):
    """  
    This allows the users to follow a club to see its newsfeed first.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        club=request.POST.get(ci)
        app_user=request.user
        club_obj=Club.objects.get(id=club)
        member=ClubFollower.objects.create(club=club_obj,app_user=app_user)
        member.save()
        return JsonResponse({'message':clubs.fcsuccess})

class UnFollowClub(APIView):
    """  
    This allows the users to unfollow a club.
    """
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        club=request.POST.get(ci)
        app_user=request.user
        club_obj=Club.objects.get(id=club)
        member=ClubFollower.objects.get(club=club_obj,app_user=app_user)
        member.delete()
        return JsonResponse({'message':clubs.ucsuccess})