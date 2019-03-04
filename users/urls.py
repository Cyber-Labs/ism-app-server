from django.urls import path,include
from . import views
from django.conf.urls import url
urlpatterns=[
    path('welcome/',view=views.Welcome.as_view()),
    path('signup/',view=views.Register.as_view()),
    path('verify_otp/',view=views.VerifyAccount.as_view()),
    path('login/',view=views.Login.as_view()),
    path('forgot_password/',view=views.ForgotPassword.as_view()),
    path('reset_password/',view=views.ResetPassword.as_view()),
    path('postnews',view=views.PostNews.as_view()),
    
]