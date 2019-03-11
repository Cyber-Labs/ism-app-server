from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics,permissions
from club.models import *
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

class Welcome(APIView):
    """ 
    This class shows a welcome message on starting of app
    """
    permission_classes=(permissions.AllowAny,)
    def get(self,request,*args,**kwargs):
        t=WelcomeModel.objects.get(id=1);
        version=t.version
        p=t.is_cumpulsory_update
        return JsonResponse({
            "success":True,
            "message":users.wsuccess,
            "version":version,
            "is_compulsory_update":p
        })

class Register(APIView):
    """  
    This class is for registration of user in app by sending a verification email.If user is already 
    registered in app then it will display a message showing already registered.
    """
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        name=request.POST.get(name_)
        email=request.POST.get(email_)
        password=request.POST.get(password_)
        if User.objects.filter(username=email).count()!=0:
            user=User.objects.get(username=email)
            if user.is_active:
                return JsonResponse({
                    'sucess':False,
                    'message':users.rfailure
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
                    'message':users.rsuccess
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
            'message':users.rsuccess
            })


class VerifyAccount(APIView):
    """ 
    This class is for verifying the email of the user by entering the otp
    in the app.
    """
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        username=request.POST.get(email_)
        otp=request.POST.get(otp_)
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
                'message':users.vsuccess,
                'access_token':token.key
            })
        else :
            return JsonResponse({
                'success':False,
                'message':users.vfailure,
                'access_token':None
            })

class Login(APIView):
    """  
    This class is for logging users in the app.
    """
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        username=request.POST.get(email_)
        password=request.POST.get(password_)
        user=authenticate(username=username,password=password)

        if user is None:
            return JsonResponse({
                'success':False,
                'message':users.lfailure,
                'access_token':None
            })
        token=Token.objects.get(user=user)
        login(request,user)
        return JsonResponse({
            'success':True,
            'message':users.lsuccess,
            'access_token':token.key
        })

class ForgotPassword(APIView):
    """
    In case the user forgots its password then it sends a otp for 
    resetting the password.
    """
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        email=request.POST.get(email_)
        if User.objects.filter(username=email).count()==0:
            return JsonResponse({
                'success':False,
                'message':users.fpfailure
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
            'message':users.fpsuccess
        })

class ResetPassword(APIView):
    """  
    This class verifies the otp for resetting password and allow users to 
    set new password.
    """
    permission_classes=(permissions.AllowAny,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        username=request.POST.get(email_)
        new_password=request.POST.get(new_password_)
        otp=request.POST.get(otp_)
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
                'message':users.rpsuccess,
                #'access_token':token.key
            })
        else :
            return JsonResponse({
                'success':False,
                'message':users.rpfailure,
                #'access_token':None
            })


class PostNews(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request,*args,**kwargs):
        club=request.POST.get(ci)
        title=request.POST.get(title_)
        short_desc=request.POST.get(sd_)
        description=request.POST.get(desc_)
        news_pic=request.FILES.get(np_)
        #user=request.user
        club_obj=Club.objects.get(id=club)
        news=News.objects.create(club=club_obj,title=title,short_desc=short_desc,description=description,news_pic=news_pic)
        news.save()
        return JsonResponse({'message':'news has been posted'})
