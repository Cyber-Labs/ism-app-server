from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics,permissions
from .models import *
from .serializers import *
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

class Welcome(APIView):
    permission_classes=(permissions.AllowAny,)
    def get(self,request,*args,**kwargs):
        t=WelcomeModel.objects.get(id=1);
        version=t.version
        p=t.is_cumpulsory_update
        return JsonResponse({
            "success":True,
            "message":'Welcome to the app',
            "version":version,
            "is_compulsory_update":p
        })

class Register(APIView):
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(username=email).count()!=0:
            user=User.objects.get(username=email)
            if user.is_active:
                return JsonResponse({
                    'sucess':False,
                    'message':'User already exist'
                })
            else:
                otp=random.randint(999,999999)
                user.set_password(password)
                user.save()
                y=UserProfile.objects.get(user=user)
                y.name=name
                y.otp=str(otp)
                y.save()
                subject='Activate your Account'

                message='Dear '+name+' Your One time Password for activation of your account is '+str(otp)+'. '
                temail=EmailMessage(subject,message,to=[email])
                temail.send()
                return JsonResponse({
                    'success':True,
                    'message':'Email verification has been sent to your email.'
                    })
        user=User.objects.create_user(username=email,password=password,email=email)
        user.is_active=False
        user.save()
        otp=random.randint(999,999999)
        y=UserProfile.objects.get(user=user)
        y.name=name
        y.otp=str(otp)
        y.save()
        token=Token.objects.create(user=user)
        subject='Activate your Account'
        
        message='Dear '+name+' Your One time Password for activation of your account is '+str(otp)+'. '
        temail=EmailMessage(subject,message,to=[email])
        temail.send()
        return JsonResponse({
            'success':True,
            'message':'Email verification has been sent to your email.'
            })


class VerifyAccount(APIView):
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        username=request.POST.get('email')
        otp=request.POST.get('otp')
        otp=str(otp)
        user=User.objects.get(username=username)
        up=UserProfile.objects.get(user=user)
        if up.otp == otp:
            user.is_active = True
            user.save()
            token=Token.objects.get(user=user)
            login(request,user)
            return JsonResponse({
                'success':True,
                'message':'OTP verified',
                'access_token':token.key
            })
        else :
            return JsonResponse({
                'success':False,
                'message':'OTP not verified',
                'access_token':None
            })

class Login(APIView):
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        username=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)

        if user is None:
            return JsonResponse({
                'success':False,
                'message':'Invalid credentials',
                'access_token':None
            })
        token=Token.objects.get(user=user)
        login(request,user)
        return JsonResponse({
            'success':True,
            'message':'Logged in Successfully',
            'access_token':token.key
        })

class ForgotPassword(APIView):
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        email=request.POST.get('email')
        if User.objects.filter(username=email).count()==0:
            return JsonResponse({
                'success':False,
                'message':'This user is not registered in app'
            })
        otp=random.randint(999,999999)
        user=User.objects.get(username=email)
        up=UserProfile.objects.get(user=user)
        up.otp=otp
        name=up.name
        up.save()
        subject='Reset Your Password'
        message='Dear '+name+' Your One time Password for resseting your password is '+str(otp)+'. '
        temail=EmailMessage(subject,message,to=[email])
        temail.send()
        return JsonResponse({
            'success':True,
            'message':'Resest password has been sent to registered email'
        })

class ResetPassword(APIView):
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        username=request.POST.get('email')
        new_password=request.POST.get('new_password')
        otp=request.POST.get('otp')
        otp=str(otp)
        user=User.objects.get(username=username)
        up=UserProfile.objects.get(user=user)
        if up.otp == otp:
            user.set_password(new_password)
            user.save()
            token=Token.objects.get(user=user)
            login(request,user)
            return JsonResponse({
                'success':True,
                'message':'Password Changed Successfully',
                #'access_token':token.key
            })
        else :
            return JsonResponse({
                'success':False,
                'message':'OTP not verified',
                #'access_token':None
            })

class ClubList(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        data=Club.objects.all().values()
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
            'message':'club list successfully sent',
            'club_list':cl,
        })

class ClubDetails(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        club=request.GET.get('club_id')
        club_obj=Club.objects.get(id=club)
        #print(club_obj,request.user)
        user=request.user
        try:
            cm=ClubMember.objects.get(club=club_obj,app_user=user)
            im=cm.is_admin
        except ClubMember.DoesNotExist:
            im=False
        img_url=request.build_absolute_uri(club_obj.club_pic.url)
        #print(img_url)
        return JsonResponse({
            'success':True,
            'message':'Club details successfully send',
            'id':club_obj.id,
            'name':club_obj.name,
            'image_url':img_url,
            'tagline':club_obj.tagline,
            'description':club_obj.description,
            'fb_link':club_obj.fb_link,
            'is_admin':im
        })

class ClubMemberList(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        club=request.GET.get('club_id')
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
            'message':'Successful',
            'member_list':ml,
        })


class AddClubMembers(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        club=request.GET.get('club_id')
        app_user=request.GET.get('email_id')
        is_admin=request.GET.get('is_admin')
        user=User.objects.get(username=app_user)
        club_obj=Club.objects.get(id=club)
        try:
            cm=ClubMember.objects.get(club=club_obj,app_user=request.user).is_admin
        except ClubMember.DoesNotExist:
            cm=False
        if cm == False:
            return JsonResponse({
                'success':False,
                'message':'Either User is not registered in app or you have not permission to add members'
            })
        if ClubMember.objects.filter(club=club_obj,app_user=user).count()!=0:
            return JsonResponse({
                'success':True,
                'message':'Member already exist in club'
            })
        member=ClubMember.objects.create(club=club_obj,app_user=user,is_admin=is_admin)
        member.save()
        return JsonResponse({
            'success':True,
            'message':'member added successfully'
        })


class RemoveClubMembers(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get(self,request,*args,**kwargs):
        club=request.GET.get('club_id')
        app_user=request.GET.get('email_id')
        user=User.objects.get(username=app_user)
        club_obj=Club.objects.get(id=club)
        try:
            cm=ClubMember.objects.get(club=club_obj,app_user=request.user).is_admin
        except ClubMember.DoesNotExist:
            cm=False
        if cm == False:
            return JsonResponse({
                'success':False,
                'message':'This is only for admins of club'
            })
        member=ClubMember.objects.get(club=club_obj,app_user=user)
        member.delete()
        return JsonResponse({
            'success':True,
            'message':'member deleted succesfully'
        })

class FollowClub(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        club=request.POST.get('club')
        app_user=request.user
        club_obj=Club.objects.get(name=club)
        member=ClubFollower.objects.create(club=club_obj,app_user=app_user)
        member.save()
        return JsonResponse({'message':'You have started following '+club+' club.'})

class UnFollowClub(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        club=request.POST.get('club')
        app_user=request.user
        club_obj=Club.objects.get(name=club)
        member=ClubFollower.objects.get(club=club_obj,app_user=app_user)
        member.delete()
        return JsonResponse({'You have just unfollowed '+club+' club.'})

class PostNews(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        club=request.POST.get('club')
        title=request.POST.get('title')
        short_desc=request.POST.get('short_desc')
        description=request.POST.get('description')
        news_pic=request.FILES.get('news_pic')
        #user=request.user
        club_obj=Club.objects.get(name=club)
        news=News.objects.create(club=club_obj,title=title,short_desc=short_desc,description=description,news_pic=news_pic)
        news.save()
        return JsonResponse({'message':'news has been posted'})

class CreateEvent(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        club=request.POST.get('club')
        title=request.POST.get('title')
        short_desc=request.POST.get('short_desc')
        description=request.POST.get('description')
        venue=request.POST.get('venue')
        event_pic=request.FILES.get('event_pic')
        event_date=request.POST.get('event_date')
        #user=request.user
        club_obj=Club.objects.get(name=club)
        print(club_obj.id)
        event=Event.objects.create(club=club_obj,title=title,short_desc=short_desc,description=description,venue=venue,event_pic=event_pic,event_start_date=event_date)
        event.save()
        return JsonResponse({'message':'news has been posted'})